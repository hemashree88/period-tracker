from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Period(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    mood = models.CharField(max_length=100, blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Convert to date objects if they’re strings
        if isinstance(self.start_date, str):
            self.start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        if isinstance(self.end_date, str):
            self.end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()

        # Now calculate duration safely
        if self.start_date and self.end_date:
            self.duration = (self.end_date - self.start_date).days

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.start_date}"
