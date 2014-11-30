
from django.shortcuts import redirect

from social.pipeline.partial import partial


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
    print is_new and not strategy.session_get('complete_profile') 
    if is_new and not strategy.session_get('complete_profile'):
        profile = strategy.session_get('profile')
        if profile:
           details.update(profile)        
           print details
           strategy.session_set('profile_complete',False)
        else:
            return redirect('social_extra_data')

