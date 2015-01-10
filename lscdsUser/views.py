from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response,redirect,render
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse,HttpResponsePermanentRedirect
import json
from django.views.generic import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from registration import signals
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView,ActivationView
from lscdsUser.forms import UserCreationForm,SocialExtraDataForm,UserProfileForm,RegistrationFormSet,NetWorkForm
from lscdsUser.models import LscdsUser
from event.models import EventType,Registration,Event
from lscds_site.decorators import render_to

from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from social.apps.django_app.utils import psa




@login_required
def event_view(request):
    registered_list = Registration.objects.filter(owner=request.user)
    dd=Event.objects.filter(registrations__owner=request.user)
    not_registered_list = Event.objects.exclude(id__in = [event.id for event in dd] )
    context = {'registered_list':registered_list,'not_registered_list':not_registered_list }
    return render(request, 'profile-event.html', context) 


@login_required
def registration_view(request):
    if 'round_table_registration' in request.POST:
          form=NetWorkForm(request.POST)
          if form.is_valid():
               return HttpResponsePermanentRedirect(reverse('profile-event'))
          else:
              return render(request, 'profile-event-registration.html', {'form':form}) 


    if request.POST and request.POST.get('event_id',None): 
       event_id= request.POST.get('event_id')
       event=Event.objects.get(pk=event_id)
       round_table = event.get_round_table()
       if event.get_round_table:
           form=NetWorkForm(initial={'event':event,'event_id':event.id})
           # Add round table choices for this particular event
           form.fields['round_table_1'].queryset = round_table
           form.fields['round_table_2'].queryset = round_table
           
           return render(request, 'profile-event-registration.html', {'form':form,'event':event}) 
       else:    
           registration,create = Registration.objects.get_or_create(owner=request.user,event=Event(pk=event_id))
           if create:
               registration.save()
           else:
               registration.delete()
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
   
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the events
        context['registered_list'] = Registration.objects.filter(owner=self.request.user)
        dd=Event.objects.filter(registrations__owner=self.request.user)
        context['not_registered_list'] = Event.objects.exclude(id__in = [event.id for event in dd] )
        return context
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(*args, **kwargs)


class LSCDSActivationView(ActivationView):
    def get_success_url(self, request, user):
        return ('profile', (), {})


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





