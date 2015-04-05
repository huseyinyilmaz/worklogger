"""Numerics Form."""
import floppyforms.__future__ as forms

from django.contrib.auth.models import User


class UserForm(forms.ModelForm):

    """User Form."""

    class Meta:
        model = User
