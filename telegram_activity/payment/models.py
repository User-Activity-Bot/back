from django.db import models

from users.models import User

class Payment(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('error', 'Error'),
        ('pending', 'Pending')
    ]
    
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    
    amount = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)