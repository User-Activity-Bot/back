import uuid

from rest_framework import serializers

from payment.models import Payment
from users.serializers import UserSerializer

class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Payment
        fields = ['id', 'user', 'status', 'amount', 'created_at']