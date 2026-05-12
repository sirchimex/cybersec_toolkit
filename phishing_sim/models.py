"""Models for Phishing Awareness Simulator."""
from django.db import models
from django.contrib.auth.models import User


class PhishingScenario(models.Model):
    """A simulated phishing email/page scenario."""
    SCENARIO_TYPES = [('email', 'Email'), ('webpage', 'Webpage')]

    title = models.CharField(max_length=200)
    scenario_type = models.CharField(max_length=10, choices=SCENARIO_TYPES, default='email')
    content = models.TextField()  # HTML content of the fake email/page
    difficulty = models.CharField(max_length=10, choices=[('easy','Easy'),('medium','Medium'),('hard','Hard')], default='medium')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class PhishingIndicator(models.Model):
    """A suspicious element within a scenario that users must identify."""
    scenario = models.ForeignKey(PhishingScenario, on_delete=models.CASCADE, related_name='indicators')
    element_id = models.CharField(max_length=50)  # CSS ID of element in content
    description = models.CharField(max_length=300)  # What makes it suspicious
    educational_tip = models.TextField()  # Detailed explanation

    def __str__(self):
        return f"{self.scenario.title}: {self.element_id}"


class UserProgress(models.Model):
    """Tracks user performance across phishing simulations."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phishing_progress')
    scenario = models.ForeignKey(PhishingScenario, on_delete=models.CASCADE)
    indicators_found = models.IntegerField(default=0)
    total_indicators = models.IntegerField(default=0)
    score_percent = models.FloatField(default=0.0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']
