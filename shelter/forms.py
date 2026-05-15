from django import forms
from .models import AdoptionApplication, Server


class AdoptionApplicationForm(forms.ModelForm):
    decibel_tolerance = forms.ChoiceField(
        choices=AdoptionApplication.DecibelTolerance.choices,
        widget=forms.RadioSelect,
        label='Noise tolerance',
    )

    class Meta:
        model = AdoptionApplication
        fields = [
            'applicant_name',
            'applicant_email',
            'applicant_location',
            'decibel_tolerance',
            'why_this_server',
        ]
        labels = {
            'applicant_name': 'Your name',
            'applicant_email': 'Your email',
            'applicant_location': 'Where would the server live?',
            'why_this_server': 'Why this particular server?',
        }
        widgets = {
            'why_this_server': forms.Textarea(attrs={'rows': 4}),
        }


class ServerFilterForm(forms.Form):
    species = forms.ChoiceField(
        choices=[('', 'Any species')] + list(Server.Species.choices),
        required=False,
    )
    size = forms.ChoiceField(
        choices=[('', 'Any size')] + list(Server.Size.choices),
        required=False,
    )
    status = forms.ChoiceField(
        choices=[('', 'All statuses')] + list(Server.Status.choices),
        required=False,
        initial='available',
    )
