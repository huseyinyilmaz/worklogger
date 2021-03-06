import datetime

from django.db.models.query import QuerySet
from django.db.models import Sum
from django.utils import timezone

from core.utils import second_to_str
from core.utils import move_by_month


class LogQuerySet(QuerySet):
    def summary_by_job(self):
        from logs.models import Job
        job_dict = dict()
        for log in self:
            job_dict.setdefault(log.job_id, []).append(log)
        job_dict = dict((Job.objects.get(id=job_id), value)
                        for job_id, value in job_dict.items())
        job_summary = [{'job': job,
                        'total_duration':
                        second_to_str(sum(log.duration
                                          for log in log_list))}
                       for job, log_list in job_dict.items()]
        return job_summary

    def total_duration(self):
        return self.aggregate(total_duration=Sum('duration'))['total_duration']

    def total_duration_display(self):
        return second_to_str(self.total_duration())

    def by_timedelta(self, start, timedelta):
        """Returns log objects that started in given timedelta"""

    def by_day(self, day):
        if not isinstance(day, datetime.datetime):
            raise Exception('day must be a datetime.datetime object')
        day = timezone.localtime(day)
        day = datetime.datetime(day.year, day.month, day.day,
                                tzinfo=day.tzinfo)
        since = day
        until = day + datetime.timedelta(days=1)

        return self.filter(start__gte=since,
                           start__lt=until)


    def by_month(self, month):
        if not isinstance(month, datetime.datetime):
            raise Exception('month must be a datetime.datetime object')
        month = timezone.localtime(month)
        since = datetime.datetime(month.year, month.month, 1,
                                  tzinfo=month.tzinfo)

        until = datetime.datetime(month.year,
                                  move_by_month(month.month, 1),
                                  1,  # day
                                  tzinfo=month.tzinfo)

        return self.filter(start__gte=since,
                           start__lt=until)
