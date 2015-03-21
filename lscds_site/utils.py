from django.core.mail import get_connection, EmailMultiAlternatives
from django.contrib import admin
from django.template import RequestContext, TemplateDoesNotExist,loader, Context
from django.contrib.sites.models import RequestSite,Site
from django.template.loader import get_template, render_to_string
from django.conf import settings



import csv

def send_event_register_mail(user,action,event,template,request=None,round_table=None):
        if Site._meta.installed:
            site = Site.objects.get_current()    
        else:
            if request is not None:
                site = RequestSite(request)   
        email_dict={}         
        if request is not None:
            email_dict = RequestContext(request, email_dict)
        subject="%s Event Registration" % (event)
        email_dict = {
            "event": event,    
            "user": user,                     
            "site": site,
            "action": action,            
        }
        if round_table is not None:
            rt1=round_table[0]
            rt2 =round_table[1]
            email_dict['rt1']=rt1
            email_dict['rt2']=rt2
        email_ctx=Context(email_dict)
        txt = get_template(template[0])
        html = get_template(template[1])
        message_txt = txt.render(email_ctx)
        message_html =html.render(email_ctx)       
        email_message = EmailMultiAlternatives(subject, message_txt, settings.DEFAULT_FROM_EMAIL, [user.email])
        
        email_message.attach_alternative(message_html, 'text/html')
        email_message.send()
        
        











from django.http import HttpResponse

def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        fields= list(modeladmin.get_list_display(request))
        opts = modeladmin.model._meta 
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(list(fields))
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)() if callable(getattr(obj, field))\
                                      else getattr(obj, field)).encode("utf-8","replace") for field in fields])
        return response
    export_as_csv.short_description = description
    return export_as_csv



def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None, 
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)

























"""
CHARSET = 'utf-8'

email.Charset.add_charset(CHARSET, email.Charset.SHORTEST, None, None)

named = lambda email, name: ('%s <%s>' % email, name) if name else email

def image_finder(tag):
    return (tag.name == u'img' or
            tag.name == u'table' and tag.has_key('background'))
    
def render(context, template):
    if template:
        t = loader.get_template(template)
        return t.render(Context(context))
    return context




def send_img_mail(subject, recipient, html,txt,
                   recipient_name='', sender_name='', sender=None,
                   CHARSET=CHARSET):
"""
"""
    If you want to use Django template system:
       use `message` and define `template`.
    
    If you want to use images in html message, no problem,
    it will attach automatically found files in html template. 
    (image paths are relative to PROJECT_PATH)
"""
"""
   # html = render(message, template)
    
    # Image processing, replace the current image urls with attached images.
    soup = BeautifulSoup(html)
    images = []
    added_images = []
    for index, tag in enumerate(soup.findAll(image_finder)):
        if tag.name == u'img':
            name = 'src'
        elif tag.name == u'table':
            name = 'background'
        # If the image was already added, skip it.
        if tag[name] in added_images:
            continue
        added_images.append(tag[name])
        images.append((tag[name], 'img%d' % index))
        tag[name] = 'cid:img%d' % index    
    html = str(soup)
    
    msg = EmailMultiAlternatives(
        subject=subject,
       txt,
        to=[named(recipient, recipient_name)],
        from_email=named(sender, sender_name),
    )
    msg.attach_alternative(html, 'text/html')    
    for filename, file_id in images:
        image_file = open(settings.PROJECT_PATH + filename, 'rb')
        msg_image = MIMEImage(image_file.read())
        image_file.close()
        msg_image.add_header('Content-ID', '<%s>' % file_id)
        msg.attach(msg_image)
    
    msg.content_subtype = "html"
    msg.send()
"""



