"""View implementations for account app."""
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


def logout_view(request):
    """Logout view."""
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/')
