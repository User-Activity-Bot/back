from rest_framework import generics, status
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer

from django.utils import timezone

class UserGetOrCreateView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user, created = User.objects.get_or_create(
            user_id=str(user_id),
        )

        user.last_active = timezone.now()
        user.save(update_fields=['last_active'])

        serializer = self.get_serializer(user)

        return Response({
            "user": serializer.data,
            "created": created
        }, status=status.HTTP_200_OK)
        