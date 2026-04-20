import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Role(models.TextChoices):
    USER = 'USER', 'User'
    ADMIN = 'ADMIN', 'Admin'


class WhitelistedEmail(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'whitelisted_emails'
        verbose_name = 'Email permitido'
        verbose_name_plural = 'Emails permitidos'

    def __str__(self):
        return self.email


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    height = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'users'


class WeightHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_history')
    weight = models.DecimalField(max_digits=5, decimal_places=1)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'weight_history'
        ordering = ['date']


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.used and (timezone.now() - self.created_at).total_seconds() < 3600

    class Meta:
        db_table = 'password_reset_tokens'
