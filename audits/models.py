from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    
    class Action(models.TextChoices):
        CREATE = 'create', 'Create'
        UPDATE = 'update', 'Update' 
        DELETE = 'delete', 'Delete'
        LOGIN = 'login', 'Login'
        LOGOUT = 'logout', 'Logout'
    
    action = models.CharField(max_length=10, choices=Action.choices)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='audit_logs',
        null=True,
        blank=True
    )
    
    model_name = models.CharField(max_length=100)  
    object_id = models.PositiveIntegerField()  
    object_repr = models.CharField(max_length=255)  
    
    changes = models.JSONField(null=True, blank=True) 
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['model_name', 'object_id']),
            models.Index(fields=['user']),
            models.Index(fields=['action']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.email if self.user else 'System'} {self.action} {self.model_name} {self.object_id} at {self.timestamp}"