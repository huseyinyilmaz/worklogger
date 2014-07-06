from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# https://djangosnippets.org/snippets/2442/
class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
