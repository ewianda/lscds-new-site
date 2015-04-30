from django.shortcuts import render,redirect
from linkedin import linkedin
from django.http import Http404
from event.models import Event,Presenter,AlumniRegistration,GuestRegistration,AdditionalGuestRegistration
from alumni.forms import AlumniRsvpForm,GuestRsvpForm,AdditionalRSVPForm
from alumni.models import AlumniTab
from lscdsUser.models import LscdsExec,MailingList
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse,HttpResponsePermanentRedirect
RETURN_URL= "http://localhost:8080/auth/linkedin/callback"
API_KEY= "75epozhfxnkl2e"
API_SECRET= "SnevZhT73Nfauqsu"
API_KEY="a8d1iaspid0q"
API_SECRET="h9xjMHDM35fD9bhG"
# Create your views here.
#selector=[{"people": {["first-name","last-name",{"positions":["id","title","is-current","company":["name"]]],"educations":["school-name"],"num-results"}]

#people=[{"people": { "id","first-name","last-name","positions":{"id","title","is-current","company":{"id","name"}},"educations":{"id","school-name",}},"num-results"}]


class AlumniTabDetailView(DetailView):
      model = AlumniTab




class AluminiRegistrationListView(ListView):
    model = GuestRegistration
    template_name= 'alumni/guest_list.html'
    
    def get_queryset(self):
        return self.model.objects.all().exclude(event__starts__lt=timezone.now())
                                                
    def get_context_data(self, **kwargs):
        context = super(AluminiRegistrationListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['alumni_list'] = AlumniRegistration.objects.all().exclude(event__starts__lt=timezone.now(),\
                                                                          ).exclude(alumni__active=True)
        context['exec_list'] = AlumniRegistration.objects.all().exclude(event__starts__lt=timezone.now(),\
                                                                          ).exclude(alumni__active=False)
        context['guest_list'] = AdditionalGuestRegistration.objects.all().exclude(event__starts__lt=timezone.now(),\
                                                                          )    
        return context
    
        
    
rsvp_message='Your have successfully registered to attend the %s event'
class LscdsExecUdateView(UpdateView):
    #paginate_by=1
    model = LscdsExec
    form_class = AlumniRsvpForm
    template_name= 'alumni/lscdsexec_update_form.html'
    fields = ['attending']
    def get_success_url(self):
        if hasattr(self, 'registration'):
            messages.add_message(self.request, messages.SUCCESS, rsvp_message % self.registration.event,) 
        elif hasattr(self, 'not_coming'):
            messages.add_message(self.request, messages.SUCCESS, "Thanks for updating your information. Hope you can make our next event ")      
        else:
            messages.add_message(self.request, messages.ERROR, "It seems registration for this event has closed."
                                                             "Please contact <a href='mailto:alumni.lscds@lscds.org'> Alumni Reception team </a> if you are having "
                                                             "difficulties")         
        return reverse('guest-list')
    
    def get_initial(self):
        return {'email':self.object.user.email}
    
    def get_context_data(self, **kwargs):
        context = super(LscdsExecUdateView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    
    def form_valid(self, form):        
        attendance = form.cleaned_data['attendance']    
        email = form.cleaned_data['email']
      
        if not form.instance.active:
            form.instance.user.email =email
            form.instance.user.save()
        event_id = self.kwargs['event']
        event = get_object_or_404(Event,pk=event_id)
        if event.registration_open:     
           if attendance:                         
                obj,created = AlumniRegistration.objects.get_or_create(event=Event(pk=event_id),alumni=form.instance)
                self.registration = obj   
                form.instance.send_email(event) 
           else:
               self.not_coming = True            
        return super(LscdsExecUdateView, self).form_valid(form)  
    
    
class GuestUdateView(UpdateView):
    #paginate_by=1
    model = Presenter
    form_class = GuestRsvpForm
    template_name= 'alumni/presenter_update_form.html'   
      
    def get_context_data(self, **kwargs):
        context = super(GuestUdateView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context 
    
    def form_valid(self, form):        
        attendance = form.cleaned_data['attendance']        
        updates= form.cleaned_data['updates']
        email = form.cleaned_data['email']
        first = self.object.name
        last = self.object.last_name
        event_id = self.kwargs['event']
        event = get_object_or_404(Event,pk=event_id)
        if event.registration_open:
            #import logging
            #logging.error(type(attendance))      
            if attendance == "True":    
               obj,created = GuestRegistration.objects.get_or_create(event=Event(pk=event_id),guest=form.instance)
               self.registration = obj # Save the registration object
               form.instance.send_email(event)
               
            else:
                self.not_coming = True
        if updates:
            ml,created=MailingList.objects.get_or_create(email=email,first_name=first,last_name=last)
        return super(GuestUdateView, self).form_valid(form)  
    def get_success_url(self):
        if hasattr(self, 'registration'):
            messages.add_message(self.request, messages.SUCCESS, rsvp_message % self.registration.event,) 
        elif hasattr(self, 'not_coming'):
            messages.add_message(self.request, messages.SUCCESS, "Thanks for updating your information. Hope you can make our next event ")      
        else:
            messages.add_message(self.request, messages.ERROR, "It seems registration for this event has closed."
                                                             "Please contact <a href='mailto:alumni.lscds@lscds.org'> Alumni Reception team </a> if you are having "
                                                             "difficulties") 
        return reverse('guest-list')
    
    

def rsvp_view(request,rsvp_code=None):
    if not rsvp_code:
        raise Http404("Page not found") 
    rsvpcode,event_id = rsvp_code.split('-') 
    try:
        alumni = LscdsExec.objects.get(rsvp_code=rsvp_code)
        #obj,created = AlumniRegistration.objects.get_or_create(event=Event(pk=event_id),alumni=alumni)
        #if created:
         #   obj.save()
        return HttpResponseRedirect(reverse('alumni-rsvp', kwargs={'pk':alumni.pk,'event':event_id}))
       
    except LscdsExec.DoesNotExist:
        pass    
    try:
        guest = Presenter.objects.get(rsvp_code=rsvp_code)
        return HttpResponseRedirect(reverse('guest-rsvp', kwargs={'pk':guest.pk,'event':event_id}))
       
        
    except Presenter.DoesNotExist:
        return render(request,'alumni/rsvp.html', {"success":False})
    
    
    
    
 
# THis view was used for additional alumni reception registration for personal guest inviations. 
def additional_rsvp_view(request,event_slug=None):
    if not event_slug:
        raise Http404("Page not found") 
    if request.method == "POST":
       event  = get_object_or_404(Event,slug=event_slug)   
       form = AdditionalRSVPForm(request.POST)
       if not  event.registration_open:
            messages.add_message(request, messages.ERROR, "It seems registration for this event has closed."
                                                             "Please contact <a href='mailto:alumni.lscds@lscds.org'> Alumni Reception team </a> if you are having"
                                                             " difficulties") 
            return HttpResponseRedirect(reverse('guest-list'))
        
       if form.is_valid():
           obj, created = AdditionalGuestRegistration.objects.get_or_create(event=event,**form.cleaned_data)           
           obj.save()
           obj.send_email(event)
           messages.add_message(request, messages.SUCCESS, rsvp_message % event,) 
           return HttpResponseRedirect(reverse('guest-list'))
    else:
        form = AdditionalRSVPForm()
    return render(request, 'alumni/additional_rsvp.html', {'form': form})
    
    
    
     
    

def linkedin_authentication(request):    
    authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
    
    return redirect(authentication.authorization_url)

def linkedin_callback(request):
  
    if request.method == "GET":
       code= request.GET.get("code",None)
       code = True
       if code:
          authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
             #authentication.authorization_code =code
             #token = authentication.get_access_token()
          token="AQUVIvgggNBTubY5GCb06liOZigFlQhRCMGvJvCa7WvenfwewKm-3zVrf0BR0c16hr0kUPcQBmE9_vbarWfyNlUy4fAhrjxeqAnkoKGM30wqV5yX0ZFm0F11jjbAN5YGVGA5qc60w5biQs2fJedZ6GLdXulm4nQN4lTUVUJ6fKzYkq-TcI0"
          app = linkedin.LinkedInApplication(token=token)
          alumnies = Alumni.objects.all()
          if alumnies.count()>0:
             for alumni in alumnies.iterator():
                 first_name = alumni.first_name
                 last_name = alumni.last_name
                 params = {"first-name": first_name,"last-name": last_name,"school-name":"University of Toronto"}
                 profile =    app.search_profile(selectors=[{"people": ["first-name", "email-address" , "last-name","positions","educations"]}], params=params)
                 if profile['people']['_total']==0:
                     continue
                                    
                 if profile['people']['values'][0]['positions']['_total']==0:
                     if 'emailAddress' in profile['people']['values'][0]:
                        alumni.email=profile['people']['values'][0]['emailAddress']
                        alumni.save()  
                     continue
                 positions = profile['people']['values'][0]['positions']['values']
                 if len(positions)==1:
                     alumni.position= positions[0]['title']
                     alumni.company= positions[0]['company']['name']
                 else:
                     for i in range(len(positions)):
                        if positions[i]['isCurrent'] ==True:
                            alumni.position= positions[0]['title']
                            alumni.company= positions[0]['company']['name']
                 if 'emailAddress' in profile['people']['values'][0]:
                     alumni.email=profile['people']['values'][0]['emailAddress']
                 alumni.save()                                       
                                  
                     #alumni.company= profile['companies']
    return redirect("/")  
