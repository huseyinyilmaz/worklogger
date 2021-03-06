from django.db import models

from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel

from django.contrib.auth.models import User
from django.utils import timezone

from core.utils import second_to_str
from logs.managers import LogQuerySet
# Create your models here.


class Job(TimeStampedModel):
    """
    Job that you spent time on
    """
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-created', 'name')

    def __str__(self):
        return self.name


class Log(TimeStampedModel):
    """
    Log for specific job.
    """
    user = models.ForeignKey(User)
    job = models.ForeignKey(Job)
    start = models.DateTimeField()
    finish = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField('seconds', default=0)
    objects = PassThroughManager.for_queryset_class(LogQuerySet)()

    def save(self, *args, **kwargs):
        if self.finish:
            duration_seconds = (self.finish - self.start).total_seconds()
            self.duration = duration_seconds
        else:
            self.duration = 0
        return super(Log, self).save(*args, **kwargs)

    def get_duration(self):
        if self.duration:
            duration = self.duration
        else:
            duration = (timezone.now() - self.start).total_seconds()
        return duration

    def get_duration_display(self):
        return second_to_str(self.get_duration())

    class Meta:
        ordering = ['user', 'start', 'finish']
        get_latest_by = "start"

    def __str__(self):
        return u'Log for %s: %s at (%s-%s)' % (self.user,
                                               self.job,
                                               self.start,
                                               self.finish)
