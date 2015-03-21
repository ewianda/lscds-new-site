from event.models import Registration
from django import forms
from event.models import (Event, Registration, Talk, Presenter,EventType,RoundTable,RoundTableRegistration,EventFee,EventBanner)
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,Field,Div,Hidden
from communication.models import LscdsEmail,EmailTemplate



class EmailAdminForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EmailAdminForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'
        self.helper.form_tag = False
    template = forms.ModelChoiceField(EmailTemplate.objects.all())
    event = forms.ModelChoiceField(Event.objects.all())
    from_email =  forms.ModelChoiceField(LscdsEmail.objects.all())
    subject = forms.CharField()    
    message = forms.CharField(widget=CKEditorWidget())
    
    