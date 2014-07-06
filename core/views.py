from django.views.generic.dates import ArchiveIndexView

from core.viewutils import LoginRequiredMixin
from logs.models import Log


class LogIndexArchiveView(LoginRequiredMixin, ArchiveIndexView):
    date_field = "start"
    make_object_list = True
    allow_future = True

    def get_queryset(self):
        qs = Log.objects.filter(user=self.request.user)
        return qs
