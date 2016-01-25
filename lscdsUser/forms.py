
from __future__ import unicode_literals

import datetime
import warnings

from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, \
    Div, Hidden
from django import forms, forms
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, \
    identify_hasher
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.forms import ModelChoiceField
from django.forms.models import inlineformset_factory
from django.forms.util import flatatt
from django.template import Context, loader
from django.template.loader import get_template
from django.utils import timezone
from django.utils.datastructures import SortedDict
from django.utils.encoding import force_bytes
from django.utils.html import format_html, format_html_join
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _, ugettext, ugettext_lazy as _
from event.models import CDPanels,RoundTable,Registration,Event, RoundTableRegistration,CDRegistration
from form_utils.forms import BetterModelForm
from lscdsUser.models import LscdsUser, UHNEmail, OldlscdsUser, MailingList


EXCLUDE = ('is_staff', 'service', 'avatar', 'relationship', 'date_joined', 'is_admin', 'is_active', 'uhn_email',
                      'password', 'last_login', 'groups', 'is_superuser', 'user_permissions', 'verify_key', 'expiry_date', 'is_u_of_t')


class WebUnsubscribeForm(forms.Form):
      email = forms.EmailField(help_text='A valid email address, please.')
      first_name = forms.CharField(max_length=100)
      last_name = forms.CharField()
      
      def __init__(self, *args, **kwargs):
        super(WebUnsubscribeForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-5'
        self.helper.layout.append(ButtonHolder(
                Submit('submit', 'Unsubscribe', css_class='pull-right btn btn-danger')
            ))
     
               
      def clean(self):
           self.cleaned_data = super(WebUnsubscribeForm, self).clean()        
           first = self.cleaned_data.get('first_name')
           last = self.cleaned_data.get('last_name')
           email = self.cleaned_data.get('email')
           try:               
               ml = MailingList.objects.get(email=email, first_name=first, last_name=last)
               self.cleaned_data['mail_list_pk'] = ml.pk                
           except MailingList.DoesNotExist:
               raise forms.ValidationError("The supplied Email, First and Last names where not found "
                        "in our records. Make sure they are the same with the one you use to subscribe. "
                        "If you have difficulties, please send us an email")
             
           return self.cleaned_data
                
               
               
class MailingListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MailingListForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-5'
        self.helper.layout.append(ButtonHolder(
                Submit('submit', 'Submit', css_class='pull-right btn btn-primary')
            ))

    class Meta:
               model = MailingList
               exclude=('newsletter_only',)
               
               
    def send_email(self, verify_key):
        # send email using the self.cleaned_data dictionary
        from django.contrib.sites.models import Site       
        if Site._meta.installed:
                site = Site.objects.get_current()
        else:
                site = RequestSite(request)
                
        email = self.cleaned_data['email']
        first = self.cleaned_data['first_name']
        last = self.cleaned_data['last_name']
        subject = "Life Sciences Career Development Society Mailing List Confirmation"
        email_dict = {
            "email": email,
            "key": verify_key,
            "site": site,
            "user":   "%s %s " % (first, last)             
        }
        email_ctx = Context(email_dict)
        txt = get_template('mailinglist/mailinglist_confirmation_email.txt')
        html = get_template('mailinglist/mailinglist_confirmation_email.html')
        message_txt = txt.render(email_ctx)
        message_html = html.render(email_ctx)       
        email_message = EmailMultiAlternatives(subject, message_txt, settings.DEFAULT_FROM_EMAIL, [email])
        
        email_message.attach_alternative(message_html, 'text/html')
        email_message.send()
        
       
        

class UserCreationForm(forms.ModelForm):
    """We are going to use crispy form package to make life
    easy with bootstrap3 This is not complicated just to give a desired
    layout of the registration form ."""

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-5'
        self.helper.layout = Layout(Fieldset('Registration Information',  # Legend
                      'email',
                      'password1',
                      'password2',),)
        self.helper.layout.append(
        Fieldset('Personal Information',  # Legend
                      'first_name',
                      'last_name',
                       Div('gender', css_class="col-md-6 col-md-offset-2", placeholder='Gender')),
        )
        self.helper.layout.append(
        Fieldset('University Affiliation',  # Legend
                     Div('university', 'faculty', css_class="col-md-6 col-md-offset-", placeholder='Gender'),
                      Div('department', 'degree', css_class="col-md-6 col-md-offset-", placeholder='Gender'),
                       Div('status', 'mailinglist', css_class="col-md-6 col-md-offset-", placeholder='Gender'),

                      ),
        )


        self.helper.layout.append(ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            ))


    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = LscdsUser
        exclude = EXCLUDE

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = OldlscdsUser.objects.filter(email=email)
        if qs.count() > 0:
            raise forms.ValidationError("A user with this email address already exist")
        return email
        
       
        
        
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SocialExtraDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SocialExtraDataForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-5'
        self.helper.layout.append(ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            ))

    class Meta:
               model = LscdsUser
               exclude = EXCLUDE + ('email', 'first_name', 'last_name')

class UserProfileForm(BetterModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-5'
        self.helper.layout.append(ButtonHolder(
                Submit('submit', 'Update Profile', css_class='button white')
            ))

    class Meta:
        model = LscdsUser
        # fields = ('first_name', 'last_name', 'university')
        exclude = EXCLUDE + ('email', 'first_name', 'last_name')
        
        
RegistrationFormSet = inlineformset_factory(LscdsUser, Registration)


class TableOneChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s , (spots remaining:%s)" % (obj, obj.session_spot(session=1))
class TableTwoChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s , (spots remaining:%s)" % (obj, obj.session_spot(session=2))
    
    
    
class CDRegistrationForm(forms.Form):
     session_1 = TableOneChoiceField(CDPanels.objects.all())
     session_2 = TableTwoChoiceField(CDPanels.objects.all())
     event = forms.CharField(widget=forms.HiddenInput())
     event_id = forms.CharField(widget=forms.HiddenInput())  
     
     def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        self.action = ''
        self.request = kwargs.pop('request', None)
        super(CDRegistrationForm, self).__init__(*args, **kwargs)
         # Bootstrap stuff for crispy forms
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout.append(FormActions(
            Div(Hidden('registration', '1'), Submit('panel', 'Register' , css_class='pull-right'), css_class='row margin-bottom-30'),
            Div(Submit('delete', 'Delete Registration', css_class=' btn-danger pull-left'),
                                    css_class='row margin-bottom-30 ')
                               ))
     
        # Filter events for a given user
        if self.event:
           panels = self.event.get_cd_pannels()
         # Add round table choices for this particular event
           self.fields['session_1'].queryset = panels
           self.fields['session_2'].queryset = panels
     
     def clean_session_2(self):
        # Check that the two password entries match
        session_1 = self.cleaned_data.get("session_1")
        session_2 = self.cleaned_data.get("session_2")
        if session_1 and  session_2  and session_1 == session_2:
            raise forms.ValidationError("You must select different session") 
        
        cd = CDRegistration.objects.filter(student=self.request.user, cd_pannel=session_2, session=2)
        if not session_2.registration_open(session=2) and cd.count() == 0:
            raise forms.ValidationError("This table is full")    
               
        return session_2
    
     def clean_session_1(self):
        # Check that the two password entries match
        session_1 = self.cleaned_data.get("session_1")
        cd = CDRegistration.objects.filter(student=self.request.user, cd_pannel=session_1, session=1)
        if not session_1.registration_open(session=1) and cd.count() == 0:
            raise forms.ValidationError("This table is full")        
        return session_1
     def save(self):
          session_1 = self.cleaned_data.get("session_1")
          session_2 = self.cleaned_data.get("session_2")
          panel1, panel2 = CDPanels.objects.get_user_panels(self.request.user, self.event)           
          if panel1 and panel2: 
              reg1 = panel1[0] 
              reg2 = panel2[0]               
              if  reg1 != session_1:          
                old_reg = CDRegistration.objects.filter(student=self.request.user, cd_pannel=reg1, session=1)
                old_reg.delete()   
                self.action = "modify"
              if reg2 != session_2:         
                old_reg = CDRegistration.objects.filter(student=self.request.user, cd_pannel=reg2, session=2)
                old_reg .delete()
                self.action = "modify"
          rt_1, cr1 = CDRegistration.objects.get_or_create(student=self.request.user, cd_pannel=session_1, session=1)
          rt_2, cr2 = CDRegistration.objects.get_or_create(student=self.request.user, cd_pannel=session_2, session=2)       
          rt_1.save()
          rt_2.save()   
     def send_mail(self):
                # Get the site information for sending emails.
         from django.contrib.sites.models import Site       
         if Site._meta.installed:
                site = Site.objects.get_current()
         else:
                site = RequestSite(request)
         rt1, rt2 = CDPanels.objects.get_user_panels(self.request.user, self.event)
         if self.action == "modify":         
            self.request.user.send_event_register_mail("modify", self.event, site, request=self.request, session=[rt1[0], rt2[0]])          
         else:
            self.request.user.send_event_register_mail("register", self.event, site, request=self.request, session=[rt1[0], rt2[0]]) 





class TableChoiceField(ModelChoiceField):
    def __init__(self, queryset,session, *args, **kwargs):
        self.session = session
        super(TableChoiceField,self).__init__(queryset, *args, **kwargs)
        
    def label_from_instance(self, obj):
        return "%s , (spots remaining:%s)" % (obj, obj.session_spot(session=self.session))
    
class NetWorkForm(forms.Form): 
     event_id = forms.CharField(widget=forms.HiddenInput())
     def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        self.request = kwargs.pop('request', None)
        super(NetWorkForm, self).__init__(*args, **kwargs)
        self.fields['event_id'].initial =self.event.id
        if self.event:
           round_table = self.event.get_round_table()
           for i in range(1,self.event.nr_session_number+1):
               table = "round_table_%s" % (i)              
               self.fields[table] =   TableChoiceField(round_table,i)               
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'      
        self.helper.layout.append(FormActions(
            Div(Submit('round_table_registration', 'Register' , css_class='pull-right'), css_class='row margin-bottom-30'),
            Div(Submit('round_table_delete', 'Delete Registration', css_class=' btn-danger pull-left'),
                                    css_class='row margin-bottom-30 ')
                               ))  
     def save(self):
         from django.contrib.sites.models import Site       
         if Site._meta.installed:
                site = Site.objects.get_current()
         else:
                site = RequestSite(self.request)
         round_tables = self.request.user.my_round_table.filter(round_table__event_id=self.event.id)
         action = 'register'
         sessions = []
         if round_tables.exists(): #Delete and create new ones
             round_tables.delete()
             action = 'modify'
             
         for key,val in   self.cleaned_data.iteritems():
             if key.startswith('round_table'):
                  vl = key.split('-')
                  session = int(key.split('_')[-1])
                  rt, cr = RoundTableRegistration.objects.get_or_create(student=self.request.user, round_table=val, session=session)
                  rt.save()
                  sessions.append(rt.round_table)
         self.request.user.send_event_register_mail(action, self.event, site, request=self.request, session=sessions)           
     def clean(self):    
              cleaned_data = super(NetWorkForm, self).clean()            
              msg = "You cannot register for the same round table more than once." 
              values = cleaned_data.values()              
              for key,val in cleaned_data.copy().iteritems():                
                  if values.count(val)>1:
                      self._errors[key]=self.error_class([msg])  
                      del cleaned_data[key]         
              return cleaned_data

class NetWorkForm2(forms.Form):
     round_table_1 = TableOneChoiceField(RoundTable.objects.all())
     round_table_2 = TableTwoChoiceField(RoundTable.objects.all())
     event = forms.CharField(widget=forms.HiddenInput())
     event_id = forms.CharField(widget=forms.HiddenInput())

     def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        self.action = ''
        self.request = kwargs.pop('request', None)
        super(NetWorkForm2, self).__init__(*args, **kwargs)
         # Bootstrap stuff for crispy forms
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout.append(FormActions(
            Div(Submit('round_table_registration', 'Register' , css_class='pull-right'), css_class='row margin-bottom-30'),
            Div(Submit('round_table_delete', 'Delete Registration', css_class=' btn-danger pull-left'),
                                    css_class='row margin-bottom-30 ')
                               ))

        # Filter events for a given user

        if self.event:
           round_table = self.event.get_round_table()
         # Add round table choices for this particular event
           self.fields['round_table_1'].queryset = round_table
           self.fields['round_table_2'].queryset = round_table
        

     def clean_round_table_2(self):
        # Check that the two password entries match
        round_table_1 = self.cleaned_data.get("round_table_1")
        round_table_2 = self.cleaned_data.get("round_table_2")
        if round_table_1 and  round_table_2  and round_table_1 == round_table_2:
            raise forms.ValidationError("You must select different guest speakers") 
        
        rt = RoundTableRegistration.objects.filter(student=self.request.user, round_table=round_table_2, session=2)
        if not round_table_2.registration_open(session=2) and rt.count() == 0:
            raise forms.ValidationError("This table is full")    
               
        return round_table_2
    
     def clean_round_table_1(self):
        # Check that the two password entries match
        round_table_1 = self.cleaned_data.get("round_table_1")
        rt = RoundTableRegistration.objects.filter(student=self.request.user, round_table=round_table_1, session=1)
        if not round_table_1.registration_open(session=1) and rt.count() == 0:
            raise forms.ValidationError("This table is full")        
        return round_table_1
     def save(self):
          round_table_1 = self.cleaned_data.get("round_table_1")
          round_table_2 = self.cleaned_data.get("round_table_2")
          rt1, rt2 = RoundTable.objects.get_user_rountable(self.request.user, self.event)           
          if rt1 and rt2: 
              reg1 = rt1[0] 
              reg2 = rt2[0]               
              if  reg1 != round_table_1:          
                old_reg = RoundTableRegistration.objects.filter(student=self.request.user, round_table=reg1, session=1)
                old_reg.delete()   
                self.action = "modify"
              if reg2 != round_table_2:         
                old_reg = RoundTableRegistration.objects.filter(student=self.request.user, round_table=reg2, session=2)
                old_reg .delete()
                self.action = "modify"
          rt_1, cr1 = RoundTableRegistration.objects.get_or_create(student=self.request.user, round_table=round_table_1, session=1)
          rt_2, cr2 = RoundTableRegistration.objects.get_or_create(student=self.request.user, round_table=round_table_2, session=2)       
          rt_1.save()
          rt_2.save() 
          
          
     def send_mail(self):
                # Get the site information for sending emails.
         from django.contrib.sites.models import Site       
         if Site._meta.installed:
                site = Site.objects.get_current()
         else:
                site = RequestSite(request)
         rt1, rt2 = RoundTable.objects.get_user_rountable(self.request.user, self.event)
         if self.action == "modify":         
            self.request.user.send_event_register_mail("modify", self.event, site, request=self.request, session=[rt1[0].guest, rt2[0].guest])          
         else:
            self.request.user.send_event_register_mail("register", self.event, site, request=self.request, session=[rt1[0].guest, rt2[0].guest])          
         

class UHNVerificationForm(forms.Form):
     choice = ModelChoiceField(UHNEmail.objects.all(), empty_label="Select email",
                                 widget=forms.Select(attrs={'class': 'form-control'}), label='Select email')
     email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder":"enter ID", 'autocomplete':'off' }), label='enter ID')

     def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")  
        super(UHNVerificationForm, self).__init__(*args, **kwargs)
         # Bootstrap stuff for crispy forms
        
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout.append(FormActions(
         Submit('session_delete', 'Send verification email'))
                               )
     def clean_email(self):
         email = self.cleaned_data.get('email', '')
         choice = self.cleaned_data.get('choice', '')
         full_email = str(email) + '@' + str(choice)    
         if full_email in [self.request.user.email ,self.request.user.uhn_email]:
            return email    
         uhn_email1 = LscdsUser.objects.filter(uhn_email=full_email)
         uhn_email2 = LscdsUser.objects.filter(email=full_email)
         if "@" in email:
            raise forms.ValidationError("ID should not contain '@'")
         if uhn_email1.count() > 0 or uhn_email2.count() > 0:                               
                raise forms.ValidationError("This email is verified as active. Contact web site admin for further assistance")
         return email






class UploadAvatarForm(forms.Form):  
    avatar = forms.ImageField()


 




