from django.urls import path
from actions.views import ActionCreateAPIView, ActionListAPIView, ActionListByUsersAPIView, GetDailyReport, ChangeAlert

urlpatterns = [
    path('create/', ActionCreateAPIView.as_view(), name='action-create'),
    
    path('alert/change/', ChangeAlert.as_view(), name='change-alert'),
    
    path('daily/', GetDailyReport.as_view(), name='daily-data'),
    path('<str:track_id>/', ActionListAPIView.as_view(), name='action-datail'),
    
    path('users/<str:user>/', ActionListByUsersAPIView.as_view(), name='action-by-user-datail')
]
