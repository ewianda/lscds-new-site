lscds-new-site
==============

Life Science Career Development Society webisite

set up
=============
In the cloned folder run 

virtualenv env

source env/bin/activate.csh

Add google app engine SDK to python path

TCSH shell
setenv PYTHONPATH PYTHONPATH:/usr/local/google_appengine/:/usr/local/google_appengine/lib/:/usr/local/google_appengine/lib/yaml-3.10/

BASH shell
export PYTHONPATH=$PYTHONPATH:/usr/local/google_appengine/:/usr/local/google_appengine/lib/:/usr/local/google_appengine/lib/yaml-3.10/

pip install Pillow 


python manage.py syncdb

python manage.py runserver

