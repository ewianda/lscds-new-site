from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from django.contrib.sites.models import get_current_site
from django.shortcuts import render_to_response,redirect,render
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse,HttpResponsePermanentRedirect
import json
from django.views.generic import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse
from django.db.models import Q,Count
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from registration import signals
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView,ActivationView
from lscdsUser.forms import UserCreationForm,UHNVerificationForm \
,SocialExtraDataForm,UserProfileForm,RegistrationFormSet,\
NetWorkForm,UploadAvatarForm
from lscdsUser.models import LscdsUser,LscdsExec
from event.models import EventType,Registration,Event,RoundTable,RoundTableRegistration
from lscds_site.decorators import render_to

from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from social.apps.django_app.utils import psa

from django.shortcuts import render
from django.core.urlresolvers import reverse
# Create your views here.

from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin

@csrf_exempt
@login_required
def ajax_mailing_list(request):
    if request.is_ajax():
        data= request.POST.get('data',None)
        print request.POST
        print data == "Yes"     
        if   data == "Yes":          
             request.user.mailinglist = True
             request.user.save()
             message = "success" 
        elif data == "No":
             request.user.mailinglist = False
             request.user.save()          
             message = "success"        
        else:
            message = ""
        return HttpResponse(message)
    else:
        message = ""
    return HttpResponse(message)
      
    

def upload_file(request):
    if request.method == 'POST':               
        form = UploadAvatarForm(request.POST, request.FILES)        
        if form.is_valid():
             request.user.avatar=request.FILES['avatar']
             request.user.save()
             messages.add_message(request, messages.SUCCESS, 'Your upload  was successfully verified.',)
        else:
           messages.add_message(request, messages.ERROR, 'An error occured in the upload process.Check file format and try again or contact web team for further assistant',extra_tags='danger')
        return HttpResponsePermanentRedirect(reverse('profile-update'))  
    else:
        return HttpResponsePermanentRedirect(reverse('profile-update'))  





class UHMVerifyView(RedirectView):
    http_method_names = ['get']
    pattern_name = 'profile-event'
    def get_success_url(self):
        return reverse('profile-event')
    def get_redirect_url(self, *args, **kwargs):
        verify_key = kwargs.get('verify_key',None)

        if verify_key:
           activated_user = LscdsUser.objects.verify_user(verify_key=verify_key)
        else:
           activated_user =None
        if activated_user:
           messages.add_message(self.request, messages.SUCCESS, 'Your UHN or UTOR email  was successfully verified.',)
        else:
           messages.add_message(self.request, messages.ERROR, 'An error occured in the verification process. Please try again or contact web team for further assistant',extra_tags='danger')

        return reverse(self.pattern_name)



class UHMVerificationView(FormView):
    template_name="uhn-email-verification.html"
    form_class = UHNVerificationForm
    success_message = "An email was sent to %s. Login into your account and click on the link to verify your email"
    def get_success_url(self):
        return reverse('profile-event')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #form.send_email()
        uhn_email = str(form.cleaned_data['email']) + '@' + str(form.cleaned_data['choice'])
        site = get_current_site(self.request)
        user = self.request.user
        user = LscdsUser.objects.create_verify_key(user,uhn_email)
        site.new = site.domain
        user.send_verify_mail(site,uhn_email,request=self.request)
        messages.success(self.request, self.success_message % uhn_email)
        return super(UHMVerificationView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UHMVerificationView, self).dispatch(*args, **kwargs)

@csrf_exempt
@login_required
def event_view(request):
    user = request.user
    nr_list =Event.objects.user_nr(user)
    not_nr_list =Event.objects.user_open_nr(user)
    registered_list =Event.objects.user_events(user)
    event_history =Event.objects.user_event_history(user)
    not_registered_list =Event.objects.user_open_events(user)
    context = {'registered_list':registered_list,'not_registered_list':not_registered_list,\
               'nr_list':nr_list,'not_nr_list':not_nr_list,\
               'event_history':event_history,"now": timezone.now()}
    return render(request, 'profile-event.html', context)


from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
def first_login(request):    
    if str(request.user) == "OldlscdsUser object":
        form =  SocialExtraDataForm() # An unbound form 
        if request.method == 'POST':
           form = SocialExtraDataForm(request.POST)
           if form.is_valid():
                password= request.user.raw_password
                email= request.user.email
                first_name = request.user.first_name
                last_name = request.user.last_name
                new_user=LscdsUser.objects.create_user(email,password)
                changed = False
                protected = ('email', 'id', 'pk')
                # Update user model attributes with the new data sent by the current
                # provider. Update on some attributes is disabled by default, for
                # example username and id fields. It's also possible to disable update
                # on fields defined in SOCIAL_AUTH_PROTECTED_FIELDS.
                for name, value in form.cleaned_data.items():
                    if not hasattr(new_user, name):
                        continue
                    current_value = getattr(new_user, name, None)
                    if not current_value or name not in protected:
                        changed |= current_value != value
                        setattr(new_user, name, value)
                new_user.first_name=first_name
                new_user.last_name=last_name    
                new_user.save()
                request.user.delete()
                logout(request)
                new_user = authenticate( username=email,password=password)
                login(request,new_user)
                return HttpResponseRedirect(reverse('profile-event')) 
               #LscdsUser.objects.create_user()
        else:
                form =  SocialExtraDataForm() # An unbound form    
        return render(request,'old_lscdsusers.html', {'form': form,}) 
    else:
        return HttpResponsePermanentRedirect(reverse('profile-event')) 
    

@login_required
def registration_view(request):
    # Get the site information for sending emails.
    if Site._meta.installed:
            site = Site.objects.get_current()
    else:
            site = RequestSite(request)
    # Round table registration for Network receptions only      
    if 'round_table_registration' in request.POST:
       event_id= request.POST.get('event_id')
       event=get_object_or_404(Event , pk=event_id)
       form=NetWorkForm(request.POST,event=event)
       # check if user has paid for event
       paid = request.user.my_round_table.all()
       if paid:
           paid=paid.filter(round_table__event_id=event_id)[0].paid
       if form.is_valid():
          event_id = form.cleaned_data['event_id']
          round_table_1 = form.cleaned_data['round_table_1']
          round_table_2 = form.cleaned_data['round_table_2']
          if not request.user.is_u_of_t and not paid and event.has_fee:
               request.session['event_id'] = event_id
               request.session['round_table_1'] = round_table_1.pk
               request.session['round_table_2'] = round_table_2.pk
               return HttpResponsePermanentRedirect(reverse('paypal:payment'))
          rt_1,cr1 = RoundTableRegistration.objects.get_or_create(student=request.user,round_table=round_table_1)
          rt_2,cr2 = RoundTableRegistration.objects.get_or_create(student=request.user,round_table=round_table_2)
          rt_1.save()
          rt_2.save()
          request.user.send_event_register_mail(event,site,request)          
          return HttpResponsePermanentRedirect(reverse('profile-event'))
       else:
            return render(request, 'profile-event-registration.html', {'form':form})
    """
    Delete a Network Reception registration completely
    """
    if 'round_table_delete' in request.POST:
       event_id= request.POST.get('event_id')
       event=get_object_or_404(Event , pk=event_id)
       form=NetWorkForm(request.POST,event=event)
       if form.is_valid():
          event_id = form.cleaned_data['event_id']
          round_table_1 = form.cleaned_data['round_table_1']
          round_table_2 = form.cleaned_data['round_table_2']
          rt_1 = get_object_or_404(RoundTableRegistration,student=request.user,round_table=round_table_1)
          rt_2 = get_object_or_404(RoundTableRegistration,student=request.user,round_table=round_table_2)
          rt_1.delete()
          rt_2.delete()
          request.user.send_event_modifiction_mail(event,site,request)
          return HttpResponsePermanentRedirect(reverse('profile-event'))
       else:
            return render(request, 'profile-event-registration.html', {'form':form})

    if request.POST and request.POST.get('event_id',None):
       event_id= request.POST.get('event_id')
       event=Event.objects.get(pk=event_id)
       if event.get_round_table():
           nr_list=RoundTable.objects.filter(round_table_registrations__student=request.user,event_id=event_id)
           if nr_list:
               initial={'event':event,'event_id':event.id ,'round_table_1':nr_list[0],'round_table_2':nr_list[1]}
           else:
               initial={'event':event,'event_id':event.id}
           form=NetWorkForm(event=event,initial=initial)
           return render(request, 'profile-event-registration.html', {'form':form,'event':event})
       else:
           registration,create = Registration.objects.get_or_create(owner=request.user,event=Event(pk=event_id))
           if create:
               registration.save()
               request.user.send_event_register_mail(event,site,request)
           else:
               registration.delete()
               request.user.send_event_modifiction_mail(event,site,request)
       return HttpResponsePermanentRedirect(reverse('profile-event'))
    else:
       return HttpResponsePermanentRedirect(reverse('profile-event'))

class UserUpdateView(UpdateView):
    """
    Class that only allows authentic user to update their profile
    Composed of first_name,last_name,date_of_birth,gender,
    """
    model = LscdsUser
    form_class = UserProfileForm
    template_name = "profile-settings.html"
    success_url = "."
    def get_object(self, queryset=None):
        return self.request.user
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(*args, **kwargs)


class LSCDSActivationView(ActivationView):
    def get_success_url(self, request, user):
        return ('profile-event', (), {})


class LSCDSRegistrationView(RegistrationView):
     form_class = UserCreationForm
     def register(self, request, **cleaned_data):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.
        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.
        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.
        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.
        """
        email, password = cleaned_data['email'], cleaned_data['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(
           email, password, site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=request,
        )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        changed = False
        protected = ('email', 'id', 'pk')
        # Update user model attributes with the new data sent by the current
        # provider. Update on some attributes is disabled by default, for
        # example username and id fields. It's also possible to disable update
        # on fields defined in SOCIAL_AUTH_PROTECTED_FIELDS.
        for name, value in cleaned_data.items():
            if not hasattr(new_user, name):
                continue
            current_value = getattr(new_user, name, None)
            if not current_value or name not in protected:
                changed |= current_value != value
                setattr(new_user, name, value)
        new_user.save()
        return new_user

class ExecListView(ListView):
    """
    Class that only allows authentic user to update their profile
    Composed of first_name,last_name,date_of_birth,gender,
    """
    template_name ="lscdsexec_list.html"
    model = LscdsExec 
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExecListView, self).dispatch(*args, **kwargs)
    
    
    
    
def context(**extra):
    return dict({
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)
    }, **extra)





@render_to('home.html')
def require_email(request):
    backend = request.session['partial_pipeline']['backend']
    return context(email_required=True, backend=backend)


def social_extra_data(request):
    if request.method == 'POST':
      form = SocialExtraDataForm(request.POST)
      if form.is_valid():
          request.session['profile_complete'] = True
          request.session['profile']= dict(request.POST.iteritems())
          backend = request.session['partial_pipeline']['backend']
          return redirect(reverse('social:complete', args=(backend,)),{'post':request.POST})
    else:
        form =  SocialExtraDataForm() # An unbound form

    return render(request,'home.html', {'form': form,})





