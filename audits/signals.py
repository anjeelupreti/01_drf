# audit/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from audits.models import AuditLog
from users.models import User
from projects.models import Project

@receiver(post_save, sender=User)
@receiver(post_save, sender=Project)
def log_create_update(sender, instance, created, **kwargs):
   
    action = AuditLog.Action.CREATE if created else AuditLog.Action.UPDATE
    
    user = getattr(instance, '_audit_user', None)
    
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=sender.__name__, 
        object_id=instance.pk,
        object_repr=str(instance),
        changes={
            'action': action,
            'note': f'{sender.__name__} was {action}'
        }
    )

@receiver(post_delete, sender=User)
@receiver(post_delete, sender=Project)  
def log_delete(sender, instance, **kwargs):
    
    user = getattr(instance, '_audit_user', None)
    
    AuditLog.objects.create(
        user=user,
        action=AuditLog.Action.DELETE,
        model_name=sender.__name__,
        object_id=instance.pk,
        object_repr=str(instance),
        changes={
            'action': 'delete',
            'note': f'{sender.__name__} was deleted'
        }
    )