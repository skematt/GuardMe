from django.db import models
import django.utils.timezone as timezone

class Crime(models.Model):
    reported_time = models.DateTimeField(default=timezone.now)
    crime = models.TextField(default='')
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    address = models.TextField(default='')