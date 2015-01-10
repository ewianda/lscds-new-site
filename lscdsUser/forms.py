from lscdsUser.models import LscdsUser
from django import forms
from django.forms.models import inlineformset_factory
from event.models import Registration,RoundTable
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,Field,Div
from form_utils.forms import BetterModelForm


""" Better form Gives more flexibility template rendering than normal django forms"""




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
        self.helper.layout = Layout( Fieldset('Registration Information', # Legend
                      'email',
                      'password1',
                      'password2',),)
        self.helper.layout.append(
        Fieldset('Personal Information', # Legend
                      'first_name',
                      'last_name',
                       Div('gender', css_class="col-md-6 col-md-offset-2",placeholder='Gender') ),
        )
        self.helper.layout.append(
        Fieldset('University Affiliation', # Legend
                     Div( 'university','faculty', css_class="col-md-6 col-md-offset-",placeholder='Gender'),
                      Div('department', 'degree', css_class="col-md-6 col-md-offset-",placeholder='Gender'), 
                       Div('status', 'mailinglist', css_class="col-md-6 col-md-offset-",placeholder='Gender'), 

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
        exclude =  ('is_staff','service','relationship', 'date_joined','is_admin','is_active',
                      'password','last_login','groups','is_superuser','user_permissions')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

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
               exclude = ('is_staff', 'service','date_joined','is_admin','is_active',
                      'password','last_login','groups','is_superuser','user_permissions','first_name','last_name','email')


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
        #fields = ('first_name', 'last_name', 'university')
        exclude = ('is_staff','service','relationship', 'date_joined','is_admin','is_active',
                      'password','last_login','groups','is_superuser','user_permissions','first_name','last_name','email')


RegistrationFormSet = inlineformset_factory(LscdsUser, Registration)
from django.forms import ModelChoiceField


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return " Guest (%s) , ( %s spots left)" % (obj.guest, obj.get_spots)


class NetWorkForm(forms.Form):
     round_table_1 = MyModelChoiceField(RoundTable.objects.all())
     round_table_2 = MyModelChoiceField(RoundTable.objects.all())
     event = forms.CharField(widget=forms.HiddenInput())
     event_id = forms.CharField(widget=forms.HiddenInput())

     def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('round_table_registration', 'Register'))
        super(NetWorkForm, self).__init__(*args, **kwargs)
     def clean_round_table_2(self):
        # Check that the two password entries match
        round_table_1 = self.cleaned_data.get("round_table_1")
        round_table_2 = self.cleaned_data.get("round_table_2")
        if round_table_1 and  round_table_2  and round_table_1 == round_table_2:
            raise forms.ValidationError("You must select different guest speakers")
        return round_table_2

