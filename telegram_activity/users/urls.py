from django.urls import path

from users.views import UserGetOrCreateView

urlpatterns = [
    path('', UserGetOrCreateView.as_view(), name='user-get-or-create'),
]
