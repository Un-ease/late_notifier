from django.db import models

class LateNotification(models.Model):
    DELAY_CHOICES = [
        (10, '10 minutes'),
        (15, '15 minutes'),
        (20, '20 minutes'),
        (30, '30 minutes'),
        (45, '45 minutes'),
        (60, '1 hour'),
        (0, 'Custom'),
    ]
    
    delay_time = models.IntegerField(choices=DELAY_CHOICES)
    custom_time = models.IntegerField(null=True, blank=True)
    reason = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)
    
    @property
    def actual_delay_time(self):
        if self.delay_time == 0 and self.custom_time:
            return self.custom_time
        return self.delay_time
    
    def __str__(self):
        return f"Late arrival - {self.actual_delay_time} minutes"