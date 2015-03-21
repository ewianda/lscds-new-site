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
from event.models import EventType,Registration,Event,RoundTable,RoundTableRegistration



base_url = Site.objects.get_current().domain
notify_url = getattr(settings, ' PAYPAL_NOTIFY_URL', "http://" + base_url )

@login_required 
def event_payment(request):           
            # What you want the button to do.
    event_id = request.session.get('event_id', False)
    round_table_1_id=  request.session.get('round_table_1',False)        
    round_table_2_id=  request.session.get('round_table_2',False) 
    user_id=request.user.pk 
    # Send user, event and table information to paypal  
    custom = "%s-%s-%s-%s" % (user_id,event_id,round_table_1_id,round_table_2_id)
    if event_id and round_table_1_id and round_table_2_id:
        event=Event.objects.get(pk=event_id)
        fee=event.fee_options.all()[0]
        amount = fee.amount                     
        now = timezone.now()   
        invoice = "".join(str(now).split())
        paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": amount,
        "item_name": "Event Registration",
        "custom":custom,
        "invoice": invoice,
        "notify_url": notify_url + reverse('paypal:paypal-ipn'),
        "return_url": "http://" + base_url + reverse('profile-event'),
        "cancel_return":"http://" + base_url +reverse('profile-event'),
            }

         # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form,'amount':amount,'event':event}
        return render(request,"payment/paypal.html", context)
    else:
         return HttpResponsePermanentRedirect(reverse('profile-event'))

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.contrib.sites.models import Site

def show_me_the_money(sender, **kwargs):
  site = Site.objects.get_current()           
  ipn_obj = sender
  if ipn_obj.payment_status == ST_PP_COMPLETED:    
        custom = ipn_obj.custom
        user_id,event_id,round_table_1_id,round_table_2_id = custom.split('-')
        User=UserModel()
        student = User.objects.get(pk=user_id)
        event=Event.objects.get(pk=event_id)
        round_table_1 = RoundTable.objects.get(event=event,pk = round_table_1_id)
        round_table_2 = RoundTable.objects.get(event=event,pk = round_table_2_id)    
        rt_1,cr1 = RoundTableRegistration.objects.get_or_create(student=student,round_table=round_table_1,paid=True,session=1)
        rt_2,cr2 = RoundTableRegistration.objects.get_or_create(student=student,round_table=round_table_2,paid=True,session=2)
        rt_1.save()
        rt_2.save()
        student.send_event_register_mail("register",event,site,request=None,round_table=[round_table_1,round_table_2])           
    

   # else:
        #...

valid_ipn_received.connect(show_me_the_money)
