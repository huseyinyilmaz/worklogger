"""View implementations for numeric source."""
import json
import logging
from django.http import HttpResponse
from django.http import Http404
from django.views.generic import View
from django.conf import settings
from djangonumerics.api import get_endpoint_urls
from djangonumerics.api import get_serializer
from djangonumerics.forms import EndPointForm
from djangonumerics.serializers import SerializerException
from django.shortcuts import render

logger = logging.getLogger()


class IndexView(View):

    """numeric source interface.

    This interface lists all endpoints for current user.
    If an enpoint parameter is provided, it provides that for given interface.
    """

    form_class = EndPointForm

    def get(self, request):
        """Return endpoint data."""
        enabled = getattr(settings,
                          'DJANGO_NUMERICS_ENABLED',
                          True)
        if not enabled:
            raise Http404()
        form = self.form_class(request.GET)
        if form.is_valid():
            serializer = get_serializer()
            try:
                user, endpoint = serializer.deserialize(
                    form.cleaned_data['endpoint'])
            except SerializerException:
                logger.exception('Cannot deserialize')
                raise Http404()

            res = endpoint.func(user, *endpoint.args, **endpoint.kwargs)
            res = {
                'postfix': res.postfix,
                'data': {
                    'value': res.value,
                }
            }

            response = HttpResponse(json.dumps(res),
                                    content_type='application/json')
        else:
            endpoint_urls = get_endpoint_urls(request.user)

            response = render(self.request, 'djangonumerics/index.html',
                              {'endpoint_urls': endpoint_urls})

        return response
