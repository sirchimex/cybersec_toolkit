"""Models for File Integrity Checker."""
from django.db import models
from django.contrib.auth.models import User


class FileCheck(models.Model):
    """Records of file integrity checks."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField()  # bytes
    sha256_hash = models.CharField(max_length=64)
    expected_hash = models.CharField(max_length=64, blank=True)
    integrity_ok = models.BooleanField(null=True)  # None = no comparison made
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-checked_at']

    def __str__(self):
        return f"{self.filename} ({self.checked_at.strftime('%Y-%m-%d')})"
