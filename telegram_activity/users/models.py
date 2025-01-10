from django.db import models

class User(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('delete', 'Deleted'),
    ]
    
    user_id = models.CharField(max_length=100, unique=True)
    
    status = models.CharField(max_length=7, default='active', choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)