from django.shortcuts import render
from django.views.generic.dates import MonthArchiveView,ArchiveIndexView
from event.models import Event,EventType
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,HttpResponsePermanentRedirect
from event.forms import EmailAdminForm
from event.models import Registration,RoundTable,RoundTableRegistration,Presenter
from lscdsUser.models import LscdsUser,LscdsExec
from django.template.loader import render_to_string


class EventTypeDetailView(DetailView):
    model = EventType

    def get_context_data(self, **kwargs):
        context = super(EventTypeDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class EventTypeListView(ListView):
    #paginate_by=1
    model = EventType

    def get_context_data(self, **kwargs):
        context = super(EventTypeListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class EventArchiveIndexView(ArchiveIndexView):
     model = Event
     date_field = "starts"
     paginate_by=3



class EventDetailView(DetailView):
      model = Event
      def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

from django.template import Context,Template





@login_required    
@csrf_exempt    
def email_preview(request):
    from django.contrib.sites.models import Site       
    if Site._meta.installed:
            site = Site.objects.get_current()
    else:
            site = RequestSite(request) 
    if request.is_ajax():           
       request.session['_old_post'] = dict(request.POST.iteritems()) 
       return HttpResponse('message')
    else:
        data = request.session.get('_old_post',None)
        form =  EmailAdminForm(data)
 
        if form.is_valid():
             subject = form.cleaned_data['subject']
             message = form.cleaned_data['message']
             event = form.cleaned_data['event']
            
             user_id = data['example'];
             model =  data['model'];
             if model == 'LscdsExecAdmin':           
                 execu = LscdsExec.objects.get(pk=user_id)
                 user = execu.user
             elif model == 'PresenterAdmin':
                 user = Presenter.objects.get(pk=user_id)
                 
             else:                  
                 user =  LscdsUser.objects.get(pk=user_id)
            
              
             setattr(user ,'rsvp_code', '123ewere-8') 
             
             t=Template(message)               
             rt1,rt2=RoundTable.objects.get_user_rountable(user,event)
             if rt1.count()>0 and rt2.count()>0:             
                    c =Context({'rt1':rt1[0].guest,'rt2':rt2[0].guest,'event':event})
             else:
                    c =Context({'event':event,'site':site,"user":user})            
             message= t.render(c)
             content = {"user":user,"message":message,'site':site}                 
             return render(request, 'email/email.html', content)       
        else:
            return HttpResponse('message')
    