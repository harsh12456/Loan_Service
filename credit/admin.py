from django.contrib import admin
from .models import User, CreditScore, Loan, Billing, Payment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('aadhar_id', 'name', 'email', 'annual_income')

@admin.register(CreditScore)
class CreditScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'loan_type', 'loan_amount', 'interest_rate', 'status')

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('user', 'billing_date', 'due_date', 'min_due', 'outstanding_principal', 'interest')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'payment_date', 'amount_paid', 'status')

