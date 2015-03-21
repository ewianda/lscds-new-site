from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,HttpResponsePermanentRedirect
from communication.models import EmailTemplate
import logging
# Create your views here.
@login_required    
@csrf_exempt    
def load_template(request):
    logging.error(request.POST)        
    if request.is_ajax():           
       template_id = request.POST.get('pk',None) 
       if not template_id:
           template= '<p></p>'
       else:           
          template = EmailTemplate.objects.get(pk=template_id).content
       return HttpResponse(template)
    else:
        return  HttpResponseRedirect('/')
    
@csrf_exempt      
def send_queue_emails(request):    
    if request.method == "POST": # should run at most 1/s due to entity group limit
        key = request.POST     
        logging.error(key)
    return  HttpResponseRedirect('/')   
       
 