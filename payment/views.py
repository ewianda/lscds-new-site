import datetime

from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from paypal.pro.views import PayPalPro
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponseRedirect,HttpResponse,HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
now = timezone.now()
from registration.users import UserModel, UserModelString

from django.contrib.sites.models import Site
from event.models import MembershipFee,EventType,Registration,Event,RoundTable,RoundTableRegistration,CDPanels,CDRegistration


if not settings.DEBUG:
   base_url = Site.objects.get_current().domain
else:
     base_url='lscdsite.ngrok.io'
notify_url = getattr(settings, ' PAYPAL_NOTIFY_URL', "http://" + base_url )

@login_required 
def membership_payment(request):     
    # Send user, information to paypal  
    custom ="%s-%s-%s-%s" % (request.user.pk,'membership','dummy','dummy')  
    amount = MembershipFee.objects.first() 
    if amount:                  
        now = timezone.now()   
        invoice = "".join(str(now).split())
        paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": amount.amount,
        "item_name": "Membership Fee",
        "currency_code": "CAD", 
        "custom":custom,
        "invoice": invoice,
        "notify_url": notify_url + reverse('paypal:paypal-ipn'),
        "return_url": "http://" + base_url + reverse('profile-event'),
        "cancel_return":"http://" + base_url +reverse('profile-event'),
            }

         # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form,'amount':amount.amount,}
        return render(request,"payment/paypal.html", context)
    else:
         return HttpResponsePermanentRedirect(reverse('profile'))

@login_required 
def event_payment(request):           
            # What you want the button to do.
    event_id = request.session.get('event_id', False)
    session1_id=  request.session.get('session_1',False)        
    session2_id=  request.session.get('session_2',False) 
    user_id=request.user.pk 
    # Send user, event and table information to paypal  
    custom = "%s-%s-%s-%s" % (user_id,event_id,session1_id,session2_id)
    if event_id:
        event=Event.objects.get(pk=event_id)        
        amount = event.amount                  
        now = timezone.now()   
        invoice = "".join(str(now).split())
        paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": amount,
        "item_name": "Event Registration",
        "currency_code": "CAD", 
        "custom":custom,
        "invoice": invoice,
        "notify_url": notify_url + reverse('paypal:paypal-ipn'),
        "return_url": "http://" + base_url + reverse('profile'),
        "cancel_return":"http://" + base_url +reverse('profile'),
            }

         # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form,'amount':amount,'event':event}
        return render(request,"payment/paypal.html", context)
    else:
         return HttpResponsePermanentRedirect(reverse('profile'))

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received,payment_was_flagged
from django.contrib.sites.models import Site

def show_me_the_money(sender, **kwargs):
  site = Site.objects.get_current()           
  ipn_obj = sender
  print   ipn_obj 
  print kwargs
  if ipn_obj.payment_status == ST_PP_COMPLETED:    
        custom = ipn_obj.custom
        user_id,event_id,session1_id,session2_id = custom.split('-')
        User=UserModel()
        student = User.objects.get(pk=user_id)
        event=Event.objects.get(pk=event_id)
        if event.event_type.pk==1:
           session1 = RoundTable.objects.get(event=event,pk = session1_id)
           session2 = RoundTable.objects.get(event=event,pk = session2_id)    
           rt_1,cr1 = RoundTableRegistration.objects.get_or_create(student=student,round_table=session1,paid=True,session=1)
           rt_2,cr2 = RoundTableRegistration.objects.get_or_create(student=student,round_table=session2,paid=True,session=2)
           rt_1.save()
           rt_2.save()
           student.send_event_register_mail("register",event,site,request=None,session=[session1,session2])    
        elif event.event_type.pk==2:
           session1 = CDPanels.objects.get(event=event,pk = session1_id)
           session2 = CDPanels.objects.get(event=event,pk = session2_id)
           rt_1, cr1 = CDRegistration.objects.get_or_create(student=student, cd_pannel=session1, session=1,paid=True)
           rt_2, cr2 = CDRegistration.objects.get_or_create(student=student, cd_pannel=session2, session=2,paid=True)    
              
           rt_1.save()
           rt_2.save() 
           student.send_event_register_mail("register",event,site,request=None,session=[session1,session2])    
       
            
        elif  event_id=='membership':
             now = timezone.now()
             User=UserModel()        
             student = User.objects.get(pk=user_id)
             expire=datetime.datetime(now.year+1, now.month, now.day)  
             membership,created = Membership.objects.get_or_create(user = student)
             membership.expire=expire
             membership.paid=True
             membership.save()
        else:                    
            registration, create = Registration.objects.get_or_create(owner=student, event=event)                  
            student.send_event_register_mail("register", event, site, request=None)
                    

   # else:
        #...

valid_ipn_received.connect(show_me_the_money)
#payment_was_flagged.connect(show_me_the_money)


