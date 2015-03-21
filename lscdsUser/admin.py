from sorl.thumbnail.admin import AdminImageMixin

import adminactions.actions as actions
from communication.action import send_EMAIL
from django import forms
from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.utils.translation import ugettext, ugettext_lazy as _
from lscdsUser.models import LscdsUser, UHNEmail, OldlscdsUser, LscdsExec, \
    MailingList


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = LscdsUser
        fields = ('email',)
        
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class OldForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField()

    class Meta:
        model = OldlscdsUser
        

   # def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
       # return self.initial["password"]
    
    
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = LscdsUser
        fields = ('email', 'password', 'is_active', 'is_admin', 'is_staff', 'is_u_of_t', 'uhn_email')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LscdsUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    send_EMAIL.short_description = 'Send Newsletter'
    actions = [send_EMAIL]
    
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'gender',)}),
        (_('Academic info'), {'fields': ('university', 'faculty', 'department', 'degree', 'status',)}),

        (_('Permissions'), {'fields': ('verify_key', 'expiry_date', 'is_u_of_t', 'is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    list_display = ('email', 'uhn_email', 'first_name', 'last_name', 'is_verified', 'is_u_of_t', 'university', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
class OldLscdsUserAdmin(admin.ModelAdmin):
    form = OldForm
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')
    
class LscdsExecAdmin(admin.ModelAdmin):
      list_display = ('user', 'active', 'position', 'admin_image')
      list_filter = ('active', 'position', 'end')
      search_fields = ('user__first_name', 'user__last_name')
      send_EMAIL.short_description = 'Send RSVP'
      actions = [send_EMAIL]
      fieldsets = (
        (None, {'fields': ('user', 'position', 'avatar', 'end', 'bio')}),
        (_('Alumin information'), {'fields': ('active', 'current_position', 'company', 'rsvp_code')}),
      
       )
"""
    user = models.OneToOneField(LscdsUser)
    position = models.CharField(_('Postion'), max_length=255)
    avatar =  ImageField(_('image'), blank=True,upload_to=UPLOAD_TO)
    start  = models.DateField(_('From'), default=timezone.now)
    end  = models.DateField(_('To'), default=timezone.now)
    bio = RichTextField(blank=True, null=True)
    active = models.BooleanField( default=True)
    current_position = models.CharField(_('Postion'), max_length=255,null=True,blank=True) 
    company = models.CharField(_('Postion'), max_length=255,null=True,blank=True)
"""


class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    readonly_fields = LogEntry._meta.get_all_field_names()

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]


    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'
    
    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')


  
    
admin.site.add_action(actions.export_as_csv)  
admin.site.add_action(actions.export_as_xls)
admin.site.add_action(actions.graph_queryset)
admin.site.register(UHNEmail)
admin.site.register(OldlscdsUser, OldLscdsUserAdmin)
admin.site.register(LscdsExec, LscdsExecAdmin)

admin.site.register(MailingList)
# Now register the new UserAdmin...
admin.site.register(LscdsUser, LscdsUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
