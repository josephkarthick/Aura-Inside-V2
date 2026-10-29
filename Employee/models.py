from django.db import models
from django.conf import settings

class Calendar_Event(models.Model):
    TYPE_CHOICES = [('title','Title'),('reminder','Reminder'),('note','Note'),('todo','Todo')]
    PRIORITY_CHOICES = [('low','Low'),('normal','Normal'),('high','High')]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='title')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    reminder = models.BooleanField(default=False)
    reminder_date = models.DateTimeField(null=True, blank=True)
    cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('start',)

    def __str__(self):
        return f"{self.title} @ {self.start.isoformat()}"

