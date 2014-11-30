#main.py ' Locate in main folder
import os
import sys

# Force sys.path to have our own directory first, so we can import from it.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))
os.environ["DJANGO_SETTINGS_MODULE"] = 'lscds_site.settings'



# Google App Hosting imports.
from google.appengine.ext.webapp import util



# Force sys.path to have our own directory first, so we can import from it.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Force Django to reload its settings.
from django.conf import settings
settings._target = None

from django.core.wsgi import get_wsgi_application

def main():    
    # Create a Django application for WSGI.
    application = get_wsgi_application()

    # Run the WSGI CGI handler with that application.
    util.run_wsgi_app(application)

if __name__ == "__main__":
    main()
