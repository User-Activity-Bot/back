import datetime

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from telegram_activity.exceptions import UnprocessableEntityException, ConflictException

from telegram_activity.settings import PLANS_PRICE

from users.models import User

from payment.models import Payment

from actions.models import Action
from actions.serializers import ActionSerializer

from scylla import ZMQClient

class ActionCreateAPIView(CreateAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        user_id = data.get("user")
        plan = data.get("plan")
        track_id = data.get("track_id")
        alert = data.get("alert", False)
        
        if plan == "alert": alert = True
        elif plan == "full_data": pass
        else: alert = False
        
        payment = None
        
        try:
            user = User.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            raise UnprocessableEntityException({"user": f"User with this ID({user_id}) does not exist."})
        
        current_actions = Action.objects.filter(track_id=track_id, user=user)
        
        if current_actions.exists():
            action = current_actions.get()
            if plan != action.plan:
                amount = PLANS_PRICE.get(plan, None)
                if not amount: 
                    raise ValidationError({"plan": "Unknown plan value"})
                payment = Payment.objects.create(
                    user=user,
                    status="pending",
                    amount=amount
                )
                action.payment = payment
                action.plan = plan
                action.save()
        else:
            if plan != "free":
                amount = PLANS_PRICE.get(plan, None)
                if not amount: 
                    raise ValidationError({"plan": "Unknown plan value"})
                payment = Payment.objects.create(
                    user=user,
                    status="pending",
                    amount=amount
                )
            else:
                if Action.objects.filter(plan="free", user=user, status="active").exists():
                    raise ConflictException("You already have one free tracking")
            
            action = Action.objects.create(
                user=user,
                payment=payment, 
                track_id=track_id,
                plan=plan, 
                alert=alert
            )
        
        serializer = self.get_serializer(action)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ChangeAlert(APIView):
    def get(self, request):
        
        track_id = request.GET.get("track_id")
        user_id = request.GET.get("user")
        
        try:
            user = User.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            raise UnprocessableEntityException({"user": f"User with this ID({user_id}) does not exist."})
        
        action = Action.objects.filter(track_id=track_id, user=user).first()
        
        action.alert = not action.alert
        action.save()
        
        return Response({"alert" : action.alert})

class GetDailyReport(APIView):
    def get(self, request):
        
        username = request.GET.get("username")
        creation_date = request.GET.get("creation_date", datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
        
        scylla = ZMQClient()
        result = scylla.get_daily_report(username=username, creation_date_start=creation_date)
        
        return Response(result)

class ActionListAPIView(RetrieveAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [AllowAny]
    lookup_field = 'track_id'
    
class ActionListByUsersAPIView(ListAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs.get('user')
        return self.queryset.filter(user__user_id=user_id)