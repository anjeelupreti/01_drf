from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)  
    
    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']
    
    def __str__(self):
        return f"[{self.code}] {self.name}"

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Admin'
        COUNTRY_ADMIN = 'country_admin', 'Country Admin'
        MEMBER = 'member', 'Member'  
    
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='users'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager() 
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    @property
    def is_super_admin(self):
        return self.role == self.Role.SUPER_ADMIN
    
    @property
    def is_country_admin(self):
        return self.role == self.Role.COUNTRY_ADMIN
    
    @property
    def is_member(self):
        return self.role == self.Role.MEMBER
    
    def can_create_users_for_country(self, country):
        if self.is_super_admin: 
            return True
        elif self.is_country_admin and self.country == country: 
            return True
        return False
    
    def clean(self):
        super().clean()
        
        if self.role in [self.Role.COUNTRY_ADMIN, self.Role.MEMBER] and not self.country:
            raise ValidationError({
                'country': f'{self.get_role_display()} must be assigned to a country.'
            })
        
        if self.role == self.Role.SUPER_ADMIN and self.country:
            raise ValidationError({
                'country': 'Super Admin cannot be assigned to a country.'
            })
    
    def save(self, *args, **kwargs):
        if not self.pk and self.is_superuser:
            super().save(*args, **kwargs)
        else:
            self.full_clean()
            super().save(*args, **kwargs)