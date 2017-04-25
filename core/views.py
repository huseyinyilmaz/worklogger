import json
from django.views.generic.dates import ArchiveIndexView

from core.viewutils import LoginRequiredMixin
from logs.models import Log

from django.http import HttpResponse


class LogIndexArchiveView(LoginRequiredMixin, ArchiveIndexView):
    date_field = "start"
    make_object_list = True
    allow_future = True
    allow_empty = True

    def get_queryset(self):
        qs = Log.objects.filter(user=self.request.user)
        return qs


def numerics(request):
    response = {
        'postfix': 'Unit',
        'data': {
            'value': 123,
        }
    }

    return HttpResponse(json.dumps(response),
                        content_type='application/json')
