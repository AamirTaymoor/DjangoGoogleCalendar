from django.db import models

# Create your models here.
class CalList(models.Model):
    etag = models.CharField(max_length=100)
    c_id = models.CharField(max_length=100, unique=True)
    summary = models.CharField(max_length=1000)
    #description = models.CharField(max_length=1000)
    timezone = models.CharField(max_length=500)
    accessrole = models.CharField(max_length=500)
    
class EventList(models.Model):
    ev_id = models.CharField(max_length=500, unique=True)
    etag = models.CharField(max_length=100)
    creator=models.CharField(max_length=500, null=True)
    start_time = models.CharField(max_length= 100, null=True)
    end_time = models.CharField(max_length= 100, null=True)
    event_link = models.CharField(max_length=500, null=True)