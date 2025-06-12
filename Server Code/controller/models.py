from django.db import models
from django.utils import timezone

# The main Timer Model
class Timer(models.Model):
    started_at = models.DateTimeField(default=timezone.now)
    duration_seconds = models.IntegerField(default=300)  # default: 5 minutes

    def __str__(self):
        return f'{self.duration_seconds / 60} Minute timer started at {self.started_at}.'
