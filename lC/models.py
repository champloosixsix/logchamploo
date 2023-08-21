from django.db import models
from django.utils import timezone


class Log(models.Model):
    log_date = models.DateField('logdate')
    name = models.CharField(max_length=200)
    steamid = models.CharField(max_length=200)
    action = models.CharField(max_length=200)
    time = models.TimeField('logtime')
    
    def __str__(self):
        return str(self.log_date)

