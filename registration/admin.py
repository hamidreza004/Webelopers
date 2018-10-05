from django.contrib import admin

# Register your models here.
from registration.models import Team, Participant, Payment


def send_mail(modeladmin, request, queryset):
    for t in queryset.all():
        t.mail_password()


send_mail.short_description = 'Send password to team members'


class TeamAdmin(admin.ModelAdmin):
    list_display = ['title', 'first_member', 'second_member']
    actions = [send_mail]


admin.site.register(Team, TeamAdmin)
admin.site.register(Participant)
admin.site.register(Payment)
