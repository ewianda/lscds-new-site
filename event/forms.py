from event.models import Registration
from django import forms


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Registration
        #fields = ('first_name', 'last_name', 'university')
        widgets = {'event': forms.HiddenInput()}

