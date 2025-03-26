from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserView, ApplyLoanView, PaymentViewSet, get_statement, BillingViewSet

# ✅ Create a router and register all viewsets
router = DefaultRouter()
router.register(r'billing', BillingViewSet, basename='billing')
router.register(r'payment', PaymentViewSet, basename='payment') 

urlpatterns = [
    path('register-user/', RegisterUserView.as_view(), name='register-user'),
    path('apply-loan/', ApplyLoanView.as_view(), name='apply-loan'),
    path('get-statement/<int:user_id>/', get_statement, name='get-statement'),
    path('', include(router.urls)),  # Include router URLs
]






