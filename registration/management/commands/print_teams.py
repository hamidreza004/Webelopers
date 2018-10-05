from django.core.management.base import BaseCommand

from registration.models import Team


def print_participant(participant):
    print(participant.national_id)
    print(participant.first_name, participant.last_name)
    print(participant.email)


def print_team(team):
    print(team.title)
    print(team.password)
    print_participant(team.first_member)
    print_participant(team.second_member)


class Command(BaseCommand):
    help = "prints a list of all teams and participants"

    def handle(self, *args, **kwargs):
        inp = input()
        for team in Team.objects.filter(grade=inp).all():
            team.save()  # to make sure there is no team without password
            print_team(team)
