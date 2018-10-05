from django import forms
from django.forms.formsets import BaseFormSet
from django.utils.translation import gettext_lazy as _

from registration.models import Participant
from .models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['title', 'grade', ]


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'


class BaseParticipantFormSet(BaseFormSet):
    def clean(self):
        """Checks that no two participants have the same National ID No."""
        if any(self.errors):
            return
        national_ids = []
        for form in self.forms:
            national_id = form.cleaned_data.get('national_id')
            if national_id in national_ids:
                form.add_error('national_id', _("Participants in a team must have distinct National ID No.s"))
                raise forms.ValidationError(_("Participants in a team must have distinct National ID No.s"))
            national_ids.append(national_id)
        super(BaseParticipantFormSet, self).clean()
