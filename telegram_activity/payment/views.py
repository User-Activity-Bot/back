from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from telegram_activity.exceptions import UnprocessableEntityException, ConflictException

from users.models import User

from payment.models import Payment
from payment.serializers import PaymentSerializer

class PaymentRetrieveAPIView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        user_id = data.get("user")
        amount = data.get("amount")
        
        if not user_id:
            raise ValidationError({"user": "This field is required."})
        if not amount:
            raise ValidationError({"amount": "This field is required."})
        
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise UnprocessableEntityException({"user": f"User with this ID({user_id}) does not exist."})
        
        if amount < 1:
            raise ValidationError({"amount": "Amount must be greater than 1."})

        
        payment = Payment.objects.create(
            user=user,
            status="pending",
            amount=amount,
        )
        
        serializer = self.get_serializer(payment)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class PaymentUpdateStatusAPIView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]
    
    def update(self, request, *args, **kwargs):
        payment = self.get_object()

        if payment.status == "pending":
            payment.status = "success"
            payment.save()
        else:
            raise ConflictException("Cannot change status. Current status is not 'pending'.")

        serializer = self.get_serializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)