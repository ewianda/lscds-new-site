lscds-new-site
==============

Life Science Career Development Society webisite

set up
======
In the cloned folder run 

virtualenv env

TCSH shell
==================
source env/bin/activate.csh

Add google app engine SDK to python path

setenv PYTHONPATH PYTHONPATH:/usr/local/google_appengine/:/usr/local/google_appengine/lib/:/usr/local/google_appengine/lib/yaml-3.10/

BASH shell
===============
source env/bin/activate.csh

Add google app engine SDK to python path

export PYTHONPATH=$PYTHONPATH:/usr/local/google_appengine/:/usr/local/google_appengine/lib/:/usr/local/google_appengine/lib/yaml-3.10/

Install Pillow only
===================
pip install Pillow 


python manage.py syncdb

python manage.py runserver

