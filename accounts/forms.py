import floppyforms.__future__ as forms

from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
