"""Models for Encryption Tool app."""
from django.db import models
from django.contrib.auth.models import User


class EncryptionLog(models.Model):
    """Logs encryption/decryption operations (without storing sensitive data)."""
    OPERATION_CHOICES = [('encrypt', 'Encrypt'), ('decrypt', 'Decrypt')]
    TYPE_CHOICES = [('xor', 'XOR'), ('aes', 'AES')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    encryption_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    performed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-performed_at']
