from rest_framework import serializers
from .models import User, CreditScore, Loan, Payment, Billing

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
    
    def validate_loan_amount(self, value):
        if value > 500000:
            raise serializers.ValidationError("Loan amount cannot exceed ₹5,00,000")
        return value
    
    def validate_interest_rate(self, value):
        if value <= 0 or value > 50:
            raise serializers.ValidationError("Interest rate must be between 0 and 50")
        return value
    
    def validate_term_period(self, value):
        if value <= 0 or value > 360:
            raise serializers.ValidationError("Term period must be between 1 and 360 months")
        return value
    


class CreditScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditScore
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = '__all__'
