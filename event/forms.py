from event.models import Registration
from django import forms
from event.models import (Event, Registration, Talk, Presenter,EventType,RoundTable,RoundTableRegistration,EventFee,EventBanner)
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,Field,Div,Hidden
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Registration
        #fields = ('first_name', 'last_name', 'university')
        widgets = {'event': forms.HiddenInput()}

class EmailAdminForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EmailAdminForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-1'
        self.helper.field_class = 'col-md-11'
        self.helper.form_tag = False
        
    event = forms.ModelChoiceField(Event.objects.all())
    subject = forms.CharField()    
    message = forms.CharField(widget=CKEditorWidget())
    