import floppyforms.__future__ as forms

from logs.models import Log
from logs.models import Job
from django.utils.formats import get_format


class SplitDateTimeWidgetNoSecond(forms.SplitDateTimeWidget):
    def __init__(self, *args, **kwargs):
        # '%H:%M'
        time_format = get_format('TIME_INPUT_FORMATS')[2]
        kwargs['time_format'] = time_format
        return super(SplitDateTimeWidgetNoSecond, self).__init__(*args,
                                                                 **kwargs)


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ('user', 'job', 'start', 'finish')
        widgets = {
            'user': forms.HiddenInput,
            'job': forms.Select,
            'start': SplitDateTimeWidgetNoSecond,
            'finish': SplitDateTimeWidgetNoSecond,
            }

    def clean(self):
        data = super(LogForm, self).clean()
        if (not data['finish'] and
            Log.objects.filter(user=data['user'],
                               finish__isnull=True).exists()):
            log = Log.objects.filter(user=data['user'],
                                     finish__isnull=True)[0]
            # if instance that we are changing is already opened instance,
            # do not raise validation error
            if log != self.instance:
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
        fields = "__all__"
        widgets = {
            'user': forms.HiddenInput,
            }
