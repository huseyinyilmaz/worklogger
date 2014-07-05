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
    start = models.DateTimeField()
    finish = models.DateTimeField()
    duration = models.IntegerField('minutes', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        duration_seconds = (self.finish - self.start).total_seconds()
        self.duration = duration_seconds
        return super(Log, self).save(*args, **kwargs)

    class Meta:
        ordering = ['user', '-start', '-finish']

    def __unicode__(self):
        return u'Log for %s: %s at (%s-%s)' % (self.user,
                                               self.job,
                                               self.start,
                                               self.finish)
