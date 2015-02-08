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
    if not h:
        return False        
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
            old_lscds_user = OldlscdsUser.objects.get(email = username)
            pwd_valid = correct_password(username,password,old_lscds_user.password)
        except OldlscdsUser.DoesNotExist:
            old_lscds_user = None  
      
        if old_lscds_user and pwd_valid: 
            try:
               new_user = LscdsUser.objects.get(email=username)  
            except LscdsUser.DoesNotExist:
                password=  old_lscds_user.raw_password
                email=  old_lscds_user.email
                first_name =  old_lscds_user.first_name
                last_name =  old_lscds_user.last_name
                new_user=LscdsUser.objects.create_user(email,password)                
                new_user.first_name=first_name
                new_user.last_name=last_name    
                new_user.save()
                old_lscds_user.delete()                  
            return new_user
        return None

    def get_user(self, user_id):
        try:
            user = LscdsUser.objects.get(pk=user_id)                      
            return user
        except LscdsUser.DoesNotExist:
            return None




