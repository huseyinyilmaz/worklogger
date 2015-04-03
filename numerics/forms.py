"""Form implementations for numerics app."""
from django import forms


class EndPointForm(forms.Form):

    """Form that will used to validate endpoint view arguments."""

    endpoint = forms.CharField()
