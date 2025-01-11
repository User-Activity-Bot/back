from users.models import User

from payment.models import Payment

from django.db import models

class Action(models.Model):
    PLAN_CHOICES = [
        ('alert', 'Alert'),
        ('free', 'Free'),
        ('full_data', 'Full Data'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, null=True, blank=True)
    
    alert = models.BooleanField(default=False)
    
    track_id = models.CharField(max_length=100)
    plan = models.CharField(max_length=9, choices=PLAN_CHOICES, default="free")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)