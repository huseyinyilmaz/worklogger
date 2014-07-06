import datetime
from django import forms

from logs.models import Log


class LogForm(forms.ModelForm):
    class Meta:
        model = Log

    def __init__(self, *args, **kwargs):
        self.fields['user'].widget = forms.HiddenInput()
        return super(LogForm, self).__init__(*args, **kwargs)
