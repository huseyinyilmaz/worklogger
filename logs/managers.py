from django.db.models.query import QuerySet
from django.db.models import Sum

from core.utils import second_to_str


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
