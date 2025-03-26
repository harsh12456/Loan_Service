from django.db import models

class User(models.Model):
    aadhar_id = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    

    def __str__(self):
        return self.name

class CreditScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.score}"

class Loan(models.Model):
    LOAN_TYPE_CHOICES = [
        ('HOME', 'Home'),
        ('PERSONAL', 'Personal'),
        ('CAR', 'Car'),
        ('BUSINESS', 'Business'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPE_CHOICES)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2) 
    term_period = models.IntegerField()
    disbursement_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING") 

    def __str__(self):
        return f"{self.user.name} - {self.loan_type} - {self.loan_amount}"

class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billing_date = models.DateField()
    due_date = models.DateField()
    min_due = models.DecimalField(max_digits=12, decimal_places=2)
    outstanding_principal = models.DecimalField(max_digits=12, decimal_places=2)
    interest = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.user.name} - {self.billing_date}"

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default='PENDING')

    def __str__(self):
        return f"{self.loan.user.name} - {self.amount_paid}"



class BillingDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    billing_date = models.DateField()
    due_date = models.DateField()
    min_due = models.DecimalField(max_digits=12, decimal_places=2)
    outstanding_principal = models.DecimalField(max_digits=12, decimal_places=2)
    interest = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.user.name} - {self.billing_date}"

class DuePayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default='PENDING')

    def __str__(self):
        return f"{self.user.name} - {self.amount_due}"