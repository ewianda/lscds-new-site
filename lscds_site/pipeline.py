
from django.shortcuts import redirect
from django.http import QueryDict
from social.pipeline.partial import partial
from lscdsUser.forms import SocialExtraDataForm

@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            return redirect('require_email')

@partial
def social_extra_data(strategy, details, user=None, is_new=False, *args, **kwargs): 
    #print is_new and not strategy.session_get('complete_profile') 
    if is_new and not strategy.session_get('complete_profile') and not user:
        profile = strategy.session_get('profile')
        if profile:
           #details.update(profile)        
          # print details
           strategy.session_set('profile_complete',False)
        else:
            return redirect('social_extra_data')


@partial
def user_details_complete(strategy, details, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if user:
        profile = strategy.session_get('profile')
        if profile:
            qdict = QueryDict('')
            qdict = qdict.copy()
            qdict.update(profile)
            form = SocialExtraDataForm(qdict,instance=user)
            if form.is_valid():
                #print form
                form.save()
            


from django.contrib.auth import logout
def social_user(backend, uid, user=None, *args, **kwargs):
    '''OVERRIDED: It will logout the current user
    instead of raise an exception '''

    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    if social:
        if user and social.user != user:
            logout(backend.strategy.request)
            #msg = 'This {0} account is already in use.'.format(provider)
            #raise AuthAlreadyAssociated(backend, msg)
        elif not user:
            user = social.user
    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': False}

from lscdsUser.models import  LscdsUser
def associate_by_email(backend, details, user=None, *args, **kwargs):
    """
    Associate current auth with a user with the same email address in the DB.
    This pipeline entry is not 100% secure unless you know that the providers
    enabled enforce email verification on their side, otherwise a user can
    attempt to take over another user account by using the same (not validated)
    email address on some provider.  This pipeline entry is disabled by
    default.
    """
    if user:
        return None

    email = details.get('email')
    if email:
        # Try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned.
        users = list(backend.strategy.storage.user.get_users_by_email(email))
        if len(users) == 0:
            u = LscdsUser.objects.filter(email__iexact=email)
            if u:
                return {'user': u[0]}
            else:
                return None
        elif len(users) > 1:
            raise AuthException(
                backend,
                'The given email address is associated with another account'
            )
        else:
            return {'user': users[0]}


