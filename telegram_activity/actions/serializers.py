import uuid

from rest_framework import serializers

from actions.models import Action

from payment.serializers import PaymentSerializer
from users.serializers import UserSerializer

class ActionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    payment = PaymentSerializer()
    
    class Meta:
        model = Action
        fields = ['id', 'user', 'payment', 'status', 'track_id', 'plan', 'created_at']