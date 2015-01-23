from django.shortcuts import render
from django.core.urlresolvers import reverse
# Create your views here.
from contact.forms import ContactForm
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
class ContactView(SuccessMessageMixin,FormView):
    template_name="contact/contact.html"
    form_class = ContactForm  
    success_message = "Your message was sent successfully"   
    def get_success_url(self):
        return reverse('contact')
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(ContactView, self).form_valid(form)