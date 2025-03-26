from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import User, CreditScore, Loan, Billing, Payment
from .serializers import UserSerializer, LoanSerializer, BillingSerializer, PaymentSerializer
from math import pow
from decimal import Decimal
from asgiref.sync import async_to_sync
from datetime import datetime, timedelta
import asyncio
import logging

logger = logging.getLogger(__name__)

async def calculate_credit_score(user_id):
    try:
        user = await asyncio.to_thread(User.objects.get, id=user_id)
        if user:
            score = (user.annual_income // 1000) + 300
            await asyncio.to_thread(CreditScore.objects.update_or_create, user=user, defaults={'score': score})
            logger.info(f"Credit score calculated for user ID {user.id}: {score}")
    except Exception as e:
        logger.error(f"Error calculating credit score for user ID {user_id}: {e}")

class RegisterUserView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                async_to_sync(calculate_credit_score)(user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in RegisterUserView: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ApplyLoanView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user')
            if not user_id:
                return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(id=user_id)
            credit_score = CreditScore.objects.get(user=user)
            if credit_score.score < 450:
                return Response({'error': 'Credit score too low'}, status=status.HTTP_400_BAD_REQUEST)
            if user.annual_income < 150000:
                return Response({'error': 'Annual income too low'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = LoanSerializer(data=request.data)
            if serializer.is_valid():
                loan_amount = float(serializer.validated_data['loan_amount'])
                interest_rate = float(serializer.validated_data['interest_rate'])
                term_period = float(serializer.validated_data['term_period'])
                if loan_amount > 500000:
                    return Response({'error': 'Loan amount exceeds limit'}, status=status.HTTP_400_BAD_REQUEST)
                if interest_rate <= 0:
                    return Response({'error': 'Interest rate must be greater than zero'}, status=status.HTTP_400_BAD_REQUEST)
                r = (interest_rate / 100) / 12
                emi = (loan_amount * r * pow(1 + r, term_period)) / (pow(1 + r, term_period) - 1)
                loan = serializer.save(status="PENDING")
                return Response({'loan_id': loan.id, 'emi': round(emi, 2), 'status': loan.status}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except CreditScore.DoesNotExist:
            return Response({'error': 'Credit score not available'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in ApplyLoanView: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        try:
            loan_id = request.data.get('loan')
            payment_date = request.data.get('payment_date')
            amount_paid = request.data.get('amount_paid')

            if not loan_id or not payment_date or not amount_paid:
                return Response({'error': 'Loan ID, payment date, and payment amount are required'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                amount_paid = Decimal(amount_paid)
                payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
            except Exception:
                return Response({'error': 'Invalid payment data format'},
                                status=status.HTTP_400_BAD_REQUEST)

            loan = Loan.objects.get(id=loan_id)
            if loan.status != 'PENDING':
                return Response({'error': 'Loan not approved'}, status=status.HTTP_400_BAD_REQUEST)

            billing = Billing.objects.get(user=loan.user, billing_date__lte=payment_date)
            if billing.outstanding_principal < amount_paid:
                return Response({'error': 'Payment exceeds outstanding amount'},
                                status=status.HTTP_400_BAD_REQUEST)

            billing.outstanding_principal -= amount_paid
            billing.save()

            payment = Payment.objects.create(
                loan=loan,
                payment_date=payment_date,
                amount_paid=amount_paid,
                status="COMPLETED"
            )

            return Response({
                'payment_id': payment.id,
                'status': payment.status,
                'remaining_principal': billing.outstanding_principal,
            }, status=status.HTTP_201_CREATED)

        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)
        except Billing.DoesNotExist:
            return Response({'error': 'Billing details not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in PaymentViewSet: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_statement(request, user_id):
    try:
        loans = Loan.objects.filter(user__id=user_id)
        if not loans.exists():
            return Response({'error': 'No loans found for user'}, status=status.HTTP_404_NOT_FOUND)
        statement = []
        for loan in loans:
            payments = Payment.objects.filter(loan=loan)
            billing = Billing.objects.get(user=loan.user)
            statement.append({
                'loan_id': loan.id,
                'loan_type': loan.loan_type,
                'loan_amount': loan.loan_amount,
                'interest_rate': loan.interest_rate,
                'status': loan.status,
                'payments': [{'payment_date': p.payment_date, 'amount_paid': p.amount_paid} for p in payments],
                'next_billing_date': billing.billing_date,
                'outstanding_principal': billing.outstanding_principal
            })
        return Response(statement, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching statement: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

async def generate_billing_statements():
    try:
        loans = await asyncio.to_thread(Loan.objects.filter, status='APPROVED')
        for loan in loans:
            r = float(loan.interest_rate) / 100 / 12
            emi = (loan.loan_amount * r * pow(1 + r, loan.term_period)) / (pow(1 + r, loan.term_period) - 1)
            billing_date = datetime.today().date()
            due_date = billing_date + timedelta(days=30)
            interest = loan.loan_amount * r
            principal = emi - interest
            await asyncio.to_thread(
                Billing.objects.update_or_create,
                user=loan.user,
                billing_date=billing_date,
                defaults={
                    'due_date': due_date,
                    'min_due': emi,
                    'outstanding_principal': loan.loan_amount - principal,
                    'interest': interest
                }
            )
            logger.info(f"Billing statement generated for Loan ID {loan.id}")
    except Exception as e:
        logger.error(f"Error generating billing statement: {e}")

class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            billing = serializer.save()
            return Response(BillingSerializer(billing).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def start_billing_automation():
    async_to_sync(generate_billing_statements)()


