# code generated by Appengine Toolkit
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))
# end generated code

from google.appengine.tools.devappserver2.python import sandbox
sandbox._WHITE_LIST_C_MODULES += ['_ssl', '_socket']
from lscds_site import socket as patched_socket
sys.modules['socket'] = patched_socket
socket = patched_socket

