from django import forms
from event.models import Event
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,Field,Div,Hidden
from event.models import (Event, Registration, Talk, Presenter,\
                          EventType,RoundTable,RoundTableRegistration,EventFee,EventBanner,\
                          AlumniRegistration,GuestRegistration,AdditionalGuestRegistration
                          )
from lscdsUser.models import LscdsExec
from django.utils.translation import ugettext_lazy as _




CHOICES = ((True, 'YES',), (False, 'NO',))

class  AdditionalRSVPForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdditionalRSVPForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-8'
        self.helper.form_tag = True
        self.helper.layout.append(ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            ))              
    class Meta:
               model = AdditionalGuestRegistration
               exclude =('event',)
    
    
    
    
    
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
    plus_one_coming = forms.BooleanField(label = _('Are you bringing a guest'),required=False,)
    guest_first_name = forms.CharField(max_length=100,label = _("Guest's First name"),required=False)  
    guest_last_name = forms.CharField(max_length=100,label = _("Guest's Last name"),required=False)  
    guest_email = forms.EmailField(max_length=100,label = _("Guest's  email"),required=False)  
    guest_company = forms.CharField(max_length=100,label = _("Guest's  company"),required=False)  
    guest_position = forms.CharField(max_length=100,label = _("Guest's position"),required=False)  
    plus_one =forms.CharField(widget = forms.HiddenInput(), required = False)
    def clean(self):
        cleaned_data = super(RSVPForm, self).clean()
        plus_one_coming = cleaned_data.get("plus_one_coming")
        first_name = cleaned_data.get("guest_first_name")
        last_name = cleaned_data.get("guest_last_name")
        email= cleaned_data.get("guest_email")
        company= cleaned_data.get("guest_company")
        position= cleaned_data.get("guest_position")
        if plus_one_coming and not (first_name and last_name):
            self._errors['first_name']=self.error_class(["Please include guest's first name",])  
            self._errors['last_name']=self.error_class(["Please include  guest's last name",])
        if plus_one_coming and (first_name and last_name):              
           cleaned_data['plus_one'] = ','.join([first_name,last_name,email,company,position,]) 
           print  cleaned_data['plus_one']           
        return cleaned_data
    
class AlumniRsvpForm(RSVPForm):
     email = forms.EmailField(help_text='A valid email address, please.')
     current_position = forms.CharField(help_text='For current exec enter degree title eg PhD',max_length=100, required=True,label =  _('Your Job title'))
     company = forms.CharField(help_text='For current exec enter Department',max_length=100, required=True,label = _('Your company name'))
     
     class Meta:
               model = LscdsExec
               fields = ['attendance','email','current_position','company','plus_one','plus_one_coming','guest_first_name','guest_last_name','guest_email','guest_company','guest_position']
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
                fields = ['attendance','email','position','company','updates','plus_one','plus_one_coming','guest_first_name','guest_last_name','guest_email','guest_company','guest_position']
                labels = {                  
                   'email': _('Your email'),
                   'company':   _('Your company name'),     
                   'current_position':   _('Your Job title'),     
                     }
               
               
               
               
               