import floppyforms.__future__ as forms

from logs.models import Log
from logs.models import Job


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

    def clean(self):
        data = super(LogForm, self).clean()
        if (not data['finish'] and
            Log.objects.filter(user=data['user'],
                               finish__isnull=True).exists()):
            raise forms.ValidationError('There is an already started job.')
        return data

    def __init__(self, *args, **kwargs):
        result = super(LogForm, self).__init__(*args, **kwargs)
        # get user either from instance or inital values
        if kwargs['instance']:
            user = kwargs['instance'].user
        else:
            user = kwargs['initial']['user']

        job_field = self.fields['job']
        job_field.queryset = job_field.queryset.filter(user=user)
        return result


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        widgets = {
            'user': forms.HiddenInput,
            }
