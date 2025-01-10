from django.urls import path
from actions.views import ActionCreateAPIView, ActionListAPIView, ActionListByUsersAPIView, GetDailyReport

urlpatterns = [
    path('create/', ActionCreateAPIView.as_view(), name='action-create'),
    
    path('<int:pk>/', ActionListAPIView.as_view(), name='action-datail'),
    path('daily/', GetDailyReport.as_view(), name='daily-data'),
    path('users/<str:user>/', ActionListByUsersAPIView.as_view(), name='action-by-user-datail')
]
