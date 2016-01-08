from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,HttpResponsePermanentRedirect
from django.template.loader import render_to_string

from lscdsUser.models import MailingList,OldlscdsUser
from event.models import Event
from communication.models import LscdsEmail,EmailTemplate
import logging
import csv
from communication.admin import get_list_serv
from google.appengine.api import taskqueue
from google.appengine.api import mail
from communication.forms import EmailAdminForm
from django.template import Context, Template
from django.conf import settings
# Create your views here.
@login_required    
@csrf_exempt    
def load_template(request):
          
    if request.is_ajax():           
       template_id = request.POST.get('pk',None) 
       if not template_id:
           template= '<p></p>'
       else:           
          template = EmailTemplate.objects.get(pk=template_id).content
       return HttpResponse(template)
    else:
        return  HttpResponseRedirect('/')
   
def send_email(user,site,event,email_class,template):  
     cont_html = "email/email.html"
     cont_txt = "email/email.txt"    
     c =Context({'event':event,'site':site,"user":user})  
              # Render the fields in the message  
     render_message= template.render(c)                                      
     content = {"user":user,"message":render_message,'site':site}                                         
     txt=render_to_string(cont_txt,content)
     html=render_to_string(cont_html,content)
     email_class.body=txt
     email_class.html = html 
                
     email_class.to = user.email
     email_class.send()
    
@csrf_exempt      
def send_queue_emails2(request): 
       email = request.POST.get('email',None)  
       from_email = request.POST.get('from_email',None)  
       html = request.POST.get('html',None) 
       txt = request.POST.get('txt',None)  
       subject = request.POST.get('subject',None)  
       email_message = mail.EmailMessage(sender="Life Sciences Career Development Society <" + str(from_email) + ">" )
       email_message.subject = subject 
       email_message.body=txt
       email_message.html = html
       email_message.to = email
       email_message.send()
       return  HttpResponse('message')  
   
   
   
   
@csrf_exempt      
def send_queue_emails(request):   
    from django.contrib.sites.models import Site       
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)  
        
    if request.method == "POST": # should run at most 1/s due to entity group limit
        model = request.POST.get('model',None)  
        message = request.POST.get('message',None)
        
        eventID = request.POST.get('event',None)
        event = Event.objects.get(pk=eventID)
        
        subject = request.POST.get('subject',None)
        
        from_emailID = request.POST.get('from_email',None)
        
        from_email = LscdsEmail.objects.get(pk=from_emailID)
        email_guest = request.POST.get('email_guest',None)
        
        old_users,mailing_list,users =get_list_serv()
        if  email_guest =="None":
           mailing_list =  mailing_list.exclude(newsletter_only=True)      
        
        email_class = mail.EmailMessage(sender=settings.DEFAULT_FROM_EMAIL + "<" + str(from_email) + ">" )
        template=Template(message) 
        email_class.subject = subject 
        if model == 'user':
           for user in users.iterator():
             if not user.email:
                 continue
             send_email(user,site,event,email_class,template)
        if model == 'old_user':
           for user in old_users.iterator():
             if not user.email:
                 continue
             send_email(user,site,event,email_class,template)  
        if model == 'mailin_list':
           for user in mailing_list.iterator():
             if not user.email:
                 continue
             send_email(user,site,event,email_class,template)         
        
    return  HttpResponse('message')  

 
 
 # Create your views here.
@login_required    
@csrf_exempt    
def send_listserv_email(request):     
       if request.is_ajax():            
           message = request.POST.get('message',None)
           event = request.POST.get('event',None)
           subject = request.POST.get('subject',None)
           from_email = request.POST.get('from_email',None)
           email_guest = request.POST.get('guest',None)
           params = {'message':message,'event':event,'subject':subject,'from_email':from_email,'email_guest':email_guest}
           params['model']='user'
           taskqueue.add(url='/worker/', params=params)
           params['model']='old_user'           
           taskqueue.add(url='/worker/', params=params)
           params['model']='mailing_list'           
           taskqueue.add(url='/worker/', params=params)          
          #taskqueue.add(url='/worker/', params=params)
          #taskqueue.add(url='/worker/', params={'model': 'old_user','message':message,'event':event})
          #taskqueue.add(url='/worker/', params={'model': 'mailing_list','message':message,'event':event})
       return HttpResponse('message')
       
# Create your views here.
@login_required    
@csrf_exempt    
def export_listserv(request):     
        old_users,mailing_list,users =get_list_serv()        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode("ListServ")

        writer = csv.writer(response)
        writer.writerow(['Name','Email'])
        
        for obj in users:
            name = obj.get_full_name()            
            try:
               writer.writerow([unicode(name).encode("utf-8"),obj.email])
            except:
                pass
            
        for obj in old_users:
            name = obj.get_full_name()
            
            try:
               writer.writerow([unicode(name).encode("utf-8"),obj.email])
            except:
                pass
        for obj in mailing_list:
           
           name = obj.get_full_name()            
           try:
               writer.writerow([unicode(name).encode("utf-8"),obj.email])
           except:
                pass
            
        return response
      

    
    