from django.urls import path
from payment.views import PaymentCreateAPIView, PaymentRetrieveAPIView, PaymentUpdateStatusAPIView

urlpatterns = [
    path('create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment-detail'),
    
    path('<int:pk>/success/', PaymentUpdateStatusAPIView.as_view(), name='payment-retrieve-update-status'),
]
