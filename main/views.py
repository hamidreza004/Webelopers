from django.shortcuts import render

from registration.models import Team


def home(request):
    a = 11
    return render(request, 'main/main.html', {'numberOfTeams': a + Team.objects.count()})
