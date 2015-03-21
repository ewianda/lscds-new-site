from django import forms
from event.models import Event
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,Field,Div,Hidden
from event.models import (Event, Registration, Talk, Presenter,\
                          EventType,RoundTable,RoundTableRegistration,EventFee,EventBanner,\
                          AlumniRegistration,GuestRegistration
                          )
from lscdsUser.models import LscdsExec
from django.utils.translation import ugettext_lazy as _




CHOICES = ((True, 'YES',), (False, 'NO',))
class  RSVPForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RSVPForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        #self.helper.form_class = 'form-horizontal'
        #self.helper.label_class = 'col-md-1'
        #self.helper.field_class = 'col-md-11'
        self.helper.form_tag = True
        self.helper.layout.append(ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            ))
        
    
               
    attendance =  forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)   
    
    
class AlumniRsvpForm(RSVPForm):
     email = forms.EmailField(help_text='A valid email address, please.')
     current_position = forms.CharField(help_text='For current exec enter degree title eg PhD',max_length=100, required=True,label =  _('Your Job title'))
     company = forms.CharField(help_text='For current exec enter Department',max_length=100, required=True,label = _('Your company name'))
     class Meta:
               model = LscdsExec
               fields = ['attendance','email','current_position','company']
               labels = {
                   
                   'email': _('Your email'),
                   'company':   _('Your company name'),     
                   'current_position':   _('Your Job title'),     
                     }
               
class GuestRsvpForm(RSVPForm):
     updates =  forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES,label = _('Would you like to receive updates about LSCDS, such as our annual newsletter?') ,  
                              )
     company = forms.CharField(max_length=100, required=True,label = _('Your company name'))
     position = forms.CharField(max_length=100, required=True,label =  _('Your Job title'))
     class Meta:
                model = Presenter
                fields = ['attendance','email','position','company','updates']
                labels = {                  
                   'email': _('Your email'),
                   'company':   _('Your company name'),     
                   'current_position':   _('Your Job title'),     
                     }
               
               
               
               
               