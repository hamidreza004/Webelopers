from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from registration.models import Team


class Command(BaseCommand):
    help = "removes the teams which haven't payed yet"

    def handle(self, *args, **kwargs):
        for team in Team.objects.filter(created_at__lte=timezone.now() - timedelta(seconds=60 * 15)).all():
            print(team.payed())
