"""Models for Password Checker app."""
from django.db import models
from django.contrib.auth.models import User


class PasswordCheck(models.Model):
    """Records each password strength check (password not stored, only metadata)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    strength_score = models.IntegerField()  # 0-100
    strength_label = models.CharField(max_length=20)  # Weak/Fair/Good/Strong
    length = models.IntegerField()
    has_uppercase = models.BooleanField(default=False)
    has_lowercase = models.BooleanField(default=False)
    has_digits = models.BooleanField(default=False)
    has_symbols = models.BooleanField(default=False)
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-checked_at']
