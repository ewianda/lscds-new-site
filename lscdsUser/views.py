from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response,redirect,render
from django.conf import settings


from registration import signals
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView
from lscdsUser.forms import UserCreationForm,SocialExtraDataForm

from lscds_site.decorators import render_to

from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from social.apps.django_app.utils import psa



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

from django.core.urlresolvers import reverse

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
