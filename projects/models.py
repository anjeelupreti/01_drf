from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Project(models.Model):
    class Status(models.TextChoices):
        PLANNING = 'planning', 'Planning'
        IN_PROGRESS = 'in_progress', 'In Progress'
        ON_HOLD = 'on_hold', 'On Hold'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNING
    )
    country = models.ForeignKey(
        'users.Country',
        on_delete=models.PROTECT,
        related_name='projects'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_projects'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='updated_projects',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def clean(self):
        super().clean()
        
        if (hasattr(self.created_by, 'role') and 
            self.created_by.role in ['country_admin', 'member'] and 
            self.created_by.country != self.country):
            raise ValidationError(
                "You can only create projects for your assigned country."
            )
    
    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)

        if self.pk and request and request.user.is_authenticated:
            self.updated_by = request.user

        self.full_clean()
        super().save(*args, **kwargs)