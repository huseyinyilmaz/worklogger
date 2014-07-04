from django.contrib import admin
from logs.models import Job, Log


class LogAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    date_hierarchy = 'day'

    list_display = ('user', 'day', 'start', 'finish', 'job')

    list_filter = ('user', 'job')


class LogInline(admin.TabularInline):
    model = Log


class JobAdmin(admin.ModelAdmin):
    inlines = [LogInline]

# Register your models here.
admin.site.register(Job, JobAdmin)
admin.site.register(Log, LogAdmin)
