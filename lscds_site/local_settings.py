import os 


#DATABSE_STR= 'mysql://root:Saflonerose=19@localhost/lscd_portal'
#DATABASE_STR= 'mysql://root@elvis-django-101:lscd/lscd_portal'


DATABASE_STR = 'mysql://root:Saflonerose=19@localhost/lscd_portal'


os.environ["DATABASE_URL"] = DATABASE_STR

import appengine_toolkit
DATABASES = {
    'default': appengine_toolkit.config(),
}
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='302804338276.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='Y6ba3RPUqhue8xl7Ap23rG8G'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='210694973168-mjrp7tt55u9jhp2b3ulmos76enbrn3a3.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='-4dpW8j3Z4de-wKwbIHkmx49'


SOCIAL_AUTH_FACEBOOK_KEY ='267923669976610'
SOCIAL_AUTH_FACEBOOK_SECRET ='d220d0fdc49c91127e7bad35172f6680'

SOCIAL_AUTH_YAHOO_OAUTH_SECRET = 'dj0yJmk9TWdES1ZKTWRhUlZuJmQ9WVdrOVp6VjBTV1Z3TXpZbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1kNw--'
SOCIAL_AUTH_YAHOO_OAUTH_KEY = '34c757a6197d59072b42d036ff6b95e3eedbcb08'


SOCIAL_AUTH_LINKEDIN_KEY='a8d1iaspid0q'
SOCIAL_AUTH_LINKEDIN_SECRET='h9xjMHDM35fD9bhG'


SOCIAL_AUTH_LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress',]
SOCIAL_AUTH_LINKEDIN_EXTRA_DATA = [('id', 'id'),
                                   ('firstName', 'first_name'),
                                   ('lastName', 'last_name'),
                                   ('emailAddress', 'email_address'),
                                   ('headline', 'headline'),
                                   ('industry', 'industry')]

SOCIAL_AUTH_TWITTER_KEY='KPfXhyUbjWwRqbRUKuwyROpCU'
SOCIAL_AUTH_TWITTER_SECRET='KY2d93DJuWHB96iGvpOJtHHuKoCu43Y6WzB0tzzDB3Ji5i1cnh'


SOCIAL_AUTH_LINKEDIN_KEY='75epozhfxnkl2e'
SOCIAL_AUTH_LINKEDIN_SECRET='SnevZhT73Nfauqsu'

EMAIL_HOST_USER     = "wiandaelvis@gmail.com"
EMAIL_HOST_PASSWORD = "Saflonerose19"

