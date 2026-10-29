# models.py
from django.db import models
from django.utils import timezone

class VoiceTask(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class VoiceSchedule(models.Model):
    task = models.ForeignKey(VoiceTask, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    times_per_hour = models.IntegerField(default=1)  # 🔴 Add this line
    voice_name = models.CharField(max_length=100, blank=True, null=True)
    voice_rate = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.task.title} ({self.start_time} - {self.end_time})"

