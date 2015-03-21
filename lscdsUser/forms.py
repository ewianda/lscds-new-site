
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
from event.models import Registration, RoundTable, RoundTableRegistration
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
        return "%s , (spots remaining:%s)" % (obj.guest, obj.session_spot(session=1))
class TableTwoChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s , (spots remaining:%s)" % (obj.guest, obj.session_spot(session=2))

class NetWorkForm(forms.Form):
     round_table_1 = TableOneChoiceField(RoundTable.objects.all())
     round_table_2 = TableTwoChoiceField(RoundTable.objects.all())
     event = forms.CharField(widget=forms.HiddenInput())
     event_id = forms.CharField(widget=forms.HiddenInput())

     def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        self.action = ''
        self.request = kwargs.pop('request', None)
        super(NetWorkForm, self).__init__(*args, **kwargs)
         # Bootstrap stuff for crispy forms
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout.append(FormActions(
            Div(Hidden('round_table_registration', '1'), Submit('round_table', 'Register' , css_class='pull-right'), css_class='row margin-bottom-30'),
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
            self.request.user.send_event_register_mail("modify", self.event, site, request=self.request, round_table=[rt1[0], rt2[0]])          
         else:
            self.request.user.send_event_register_mail("register", self.event, site, request=self.request, round_table=[rt1[0], rt2[0]])          
         

class UHNVerificationForm(forms.Form):
     choice = ModelChoiceField(UHNEmail.objects.all(), empty_label="Select email",
                                 widget=forms.Select(attrs={'class': 'form-control'}), label='Select email')
     email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder":"enter ID", 'autocomplete':'off' }), label='enter ID')

     def __init__(self, *args, **kwargs):
        super(UHNVerificationForm, self).__init__(*args, **kwargs)
         # Bootstrap stuff for crispy forms
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout.append(FormActions(
         Submit('round_table_delete', 'Send verification email'))
                               )
     def clean_email(self):
         email = self.cleaned_data.get('email', '')
         choice = self.cleaned_data.get('choice', '')
         full_email = str(email) + '@' + str(choice)         
         uhn_email1 = LscdsUser.objects.filter(uhn_email=full_email, is_u_of_t=True)
         uhn_email2 = LscdsUser.objects.filter(email=full_email)
         if "@" in email:
            raise forms.ValidationError("ID should not contain '@'")
         if uhn_email1.count() > 0 or uhn_email2.count() > 0:
             raise forms.ValidationError("This email is verified as active. Contact web site admin for further assistance")
         return email






class UploadAvatarForm(forms.Form):  
    avatar = forms.ImageField()


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-5'
        self.helper.layout.append(ButtonHolder(
                Submit('submit', 'Set Password', css_class='col-md-offset-3')
            ))
        
        

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user
    

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
         # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-5'
        self.helper.layout.append(ButtonHolder(
                Submit('submit', 'Reset Password', css_class='col-md-offset-3')
            ))
        
    def clean_email(self):
        UserModel = get_user_model()
        email = self.cleaned_data.get('email')
        qs = OldlscdsUser.objects.filter(email=email)
        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        if not (qs or active_users):
            raise forms.ValidationError("There is no account associated with this email. Please register to create an account")
        return email
    
    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            # if not user.has_usable_password():
               # continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, from_email, [user.email])
            
        old_users = OldlscdsUser.objects.filter(email=email)
        if old_users:
          for user in old_users:  
            if not user.last_login: 
              user.last_login = timezone.now()
            if not user.password:
                user.set_password('user.email')
            user.save()                     
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, from_email, [user.email])






