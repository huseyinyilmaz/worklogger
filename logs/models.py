from django.db import models
from accounts.models import User
# Create your models here.


class Job(models.Model):
    """
    Job that you spent time on
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', 'name')

    def __unicode__(self):
        return self.name


class Log(models.Model):
    """
    Log for specific job.
    """
    user = models.ForeignKey(User)
    job = models.ForeignKey(Job)
    day = models.DateField()
    start = models.TimeField()
    finish = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user', '-day', '-start', '-finish']

    def __unicode__(self):
        return u'Log for %s: %s at %s (%s-%s)' % (self.user,
                                                  self.job,
                                                  self.day,
                                                  self.start,
                                                  self.finish)
