from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

import zarinpal.functions as zarinpal
from registration.forms import TeamForm, BaseParticipantFormSet
from registration.models import Payment
from .forms import ParticipantForm
from .models import Team


# Create your views here.
def register(request):
    participants_formset = formset_factory(ParticipantForm, extra=2, formset=BaseParticipantFormSet)
    if request.method == 'POST':
        participants_forms = participants_formset(request.POST)
        team_form = TeamForm(request.POST)
        is_valid = participants_forms.is_valid() and team_form.is_valid()
        if is_valid:
            participants = [form.save(commit=True) for form in participants_forms]
            team = team_form.save(commit=False)
            team.first_member = participants[0]
            team.second_member = participants[1]
            team.payment = Payment.objects.get(active=True)
            team.transaction = zarinpal.payment_request(team.payment)
            team.save()
            return HttpResponseRedirect("https://www.zarinpal.com/pg/StartPay/{}".format(team.transaction))
    else:
        participants_forms = participants_formset()
        team_form = TeamForm()

    return render(request, 'registration/register.html', {'participants_form': participants_forms,
                                                          'team_form': team_form})


def receive_payment_feedback(request):
    team = get_object_or_404(Team, transaction=request.GET.get('Authority', '0'))
    status = team.payed()
    if status:
        return render(request, 'registration/result.html', {
            'team_name': team.title,
            'status': status,
        })
    else:
        team.first_member.delete()
        team.second_member.delete()
        team.delete()
        return render(request, 'registration/result.html', {
            'team_name': team.title,
            'status': -1,
        })
