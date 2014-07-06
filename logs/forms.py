import datetime
# from django import forms
import floppyforms.__future__ as forms

from logs.models import Log


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ('user', 'job', 'start', 'finish')
        widgets = {
            'user': forms.HiddenInput,
            'job': forms.Select,
            'start': forms.SplitDateTimeWidget,
            'finish': forms.SplitDateTimeWidget,
            }

    def __init__(self, *args, **kwargs):
        # self.fields['user'].widget = forms.HiddenInput()
        return super(LogForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(LogForm, self).clean()
        if (not data['finish'] and
            Log.objects.filter(user=data['user'],
                               finish__isnull=True).exists()):
            raise forms.ValidationError('There is an already started job.')
        return data
