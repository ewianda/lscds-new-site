from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.template import Context, Template
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.admin import helpers
from communication.forms import EmailAdminForm
from django.template.response import TemplateResponse
from django.utils import six
from google.appengine.api import mail
from google.appengine.api import taskqueue

import hashlib
import random
import re
from lscdsUser.models import LscdsExec

import logging

def send_EMAIL(modeladmin, request, queryset):
        #chuncks = [queryset[x:x+100] for x in xrange(0,queryset.count(),100)] 
       # import logging
       
       # for i in range(len(chuncks)):
           # taskqueue.add(url='/worker/', params={'key': chuncks[i]})
        
        """
        This function is an admin action function that sends emails about events
        to Lscds Exec, Presenter/Guest of events, Newsletter to mailing list.
        queryset is  the list of emails
        """
        cont_html = "email/email.html"
        cont_txt = "email/email.txt"        
        context = {'model':modeladmin.__class__.__name__ ,            
                'title': _("Send Email"),
                'queryset': queryset,
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,         

            }


        if request.POST.get('post'):
            form = EmailAdminForm(request.POST)
            if form.is_valid():
                messages = ()
                # Get the site from which the email is coming from 
                from django.contrib.sites.models import Site       
                if Site._meta.installed:
                     site = Site.objects.get_current()
                else:
                     site = RequestSite(request) 
                     
                # Read email information from submited form                    
                subject = form.cleaned_data['subject']
                form_message = form.cleaned_data['message']
                event = form.cleaned_data['event']  
                from_email= form.cleaned_data['from_email'] 
                email_message = mail.EmailMessage(sender="Life Sciences Career Development Society <" + str(from_email) + ">" )
                t=Template(form_message) 
                email_message.subject = subject 
                
                # Now loop over all emails and send the appropriate emails
                
                #for i in range(20):   
               
                for q in queryset:
                    # Check if this for session registration i.e for NR and CD events
                    if hasattr(q,"student"):
                       user = q.student
                       rt1,rt2=RoundTable.objects.get_user_rountable(user,event)              
                       c =Context({'rt1':rt1[0].guest,'rt2':rt2[0].guest,'event':event,'site':site,"user":user})
                       
                    # Check if this is for Seminar series events
                    elif hasattr(q,"owner"):
                         user = q.owner
                         c =Context({'event':event,'site':site,"user":user})
                    
                    # Check if this is for AR Guest registration
                    elif hasattr(q,"guest"):
                         user = q.guest
                         c =Context({'event':event,'site':site,"user":user})    
                   
                    # Check for AR exec/alumin registration
                    elif hasattr(q,"alumni"):
                         user = q.alumni
                         c =Context({'event':event,'site':site,"user":user})   
                         
                    # This will match Lscds Exec/Alumni and Presenters/Guest
                    else:
                        user = q
                        c =Context({'event':event,'site':site,"user":user})
                        
                    if hasattr(q,"rsvp_code"):
                        # Check if it is Lscds Exec using the user field since they are Foreign Key to Lscds Users
                        if hasattr(q,"user"):
                            email = q.user.email
                        else:
                            email = q.email 
                        # If no email is found then do nothing                           
                        if not email:
                            continue
                        salt = hashlib.sha1(six.text_type(random.random()).encode('ascii')).hexdigest()[:5]
                        salt = salt.encode('ascii')                
                        
                        
                        if isinstance(email, six.text_type):
                            email = email.encode('utf-8')
                        verify_key = hashlib.sha1(salt+email).hexdigest()
                        
                        # Generate and RSVP key an attach the event to it.
                        q.rsvp_code=verify_key + '-'+ str(event.pk)
                        q.save() 
                        
                       
                    # Render the fields in the message  
                    render_message= t.render(c)                                      
                    content = {"user":user,"message":render_message,'site':site}   
                                       
                    txt=render_to_string(cont_txt,content)
                    html=render_to_string(cont_html,content)
                    email_message.body=txt
                    email_message.html = html
                    email = user.user.email if hasattr(user,"user") else user.email
                    email_message.to = email
                    email_message.send()
                    #logging.error("Mail sent successfully")            
                modeladmin.message_user(request, "Email sent successfully sent to %s addresses" % (queryset.count()) )
              
            else:
                context.update({"form":form})
                return TemplateResponse(request, 'admin/send_email.html',
                context, current_app=modeladmin.admin_site.name)
        else:
            form = EmailAdminForm()
            context.update({"form":form})
            return TemplateResponse(request, 'admin/send_email.html',
                context, current_app=modeladmin.admin_site.name)
            
            
            
            
            
            