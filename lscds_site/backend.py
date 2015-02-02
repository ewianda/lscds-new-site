from django.conf import settings
from django.contrib.auth.models import User, check_password
import re
import hashlib
import random
import string
from lscdsUser.models import LscdsUser, OldlscdsUser
from django.utils import timezone

PASS_RE = re.compile(r"^.{6,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

def make_salt(n):
    return ''.join(random.choice(string.letters) for x in xrange(n))

def make_pw_hash(username, password, salt=None):
    # make password hash to store in the database
    if not salt:
        salt = make_salt(5)
    hash = hashlib.sha256(username + password + salt).hexdigest()
    return '%s|%s' % (hash, salt)

def correct_password(name, pw, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(name, pw, salt)



class OldUserAuthenticationBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name, and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'
    """

    def authenticate(self, username=None, password=None):
        try:            
            user = OldlscdsUser.objects.get(email = username)
            pwd_valid = correct_password(username,password,user.password)
        except OldlscdsUser.DoesNotExist:
            user = None  
      
        if user and pwd_valid:      
            user.is_active = True
            user.last_login = timezone.now()
            user.raw_password = password
            user.save()      
            return user
        return None

    def get_user(self, user_id):
        try:
            user = OldlscdsUser.objects.get(pk=user_id)
            setattr(user,'backend','OldUserAuthenticationBackend')            
            return user
        except OldlscdsUser.DoesNotExist:
            return None




