from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from loginsystem.forms import UserChangeForm,UserCreationForm
from loginsystem.models import User


# class UserAdmin(BaseUserAdmin):    #custom admin
#     list_display = ('email','username','is_admin','is_staff')               #sth that appears in the admin column
#     search_fields = ('email','username',)             #search bar in the admin console in account part
#     # readonly_fields = ('date_joined','last_login')
#
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin','username','phone_number','fullname','image')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password','username','phone_number','fullname','image')}),

        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username','password1', 'password2'),
        }),
    )
    search_fields = ('email','username')
    ordering = ('email',)
    filter_horizontal = ()


# Now login_app the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
