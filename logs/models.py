from django.db import models
from accounts.models import User
# Create your models here.


class Job(models.Model):
    """
    Job that you spent time on
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)


class Log(models.Model):
    """
    Log for specific job.
    """
    user = models.ForeignKey(User)
    job = models.ForeignKey(Job)
    start = models.DateTimeField()
    finish = models.DateTimeField()
