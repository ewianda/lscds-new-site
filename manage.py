#!/usr/bin/env python
import os
import sys


def add_appsever_import_paths():
    from dev_appserver import EXTRA_PATHS
    sys.path = EXTRA_PATHS + sys.path
    sys.path.remove("/usr/local/google_appengine/lib/django-1.4")

 
def initialize_service_apis():
    try:
            from google.appengine.tools import dev_appserver
    except ImportError:
            from google.appengine.tools import old_dev_appserver as dev_appserver
 
    from google.appengine.tools.dev_appserver_main import ParseArguments
    args, option_dict = ParseArguments('') # Otherwise the option_dict isn't populated.
    dev_appserver.SetupStubs('local', **option_dict)
    
add_appsever_import_paths()
initialize_service_apis()
sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lscds_site.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
