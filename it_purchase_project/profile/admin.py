from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm





class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
    'username', 'first_name', 'last_name', 'email', 'job_title')
    fieldsets = (
        ('Required Fields', {'fields': (
        'username', 'first_name', 'last_name', 'email', 'password',)}),
        ('Personal info', {'fields': ('job_title',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),

    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Required Fields', {'fields': (
        'username', 'first_name', 'last_name', 'email', 'password1',
        'password2')}),
        ('Personal info', {'fields': ('job_title',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),

    )
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('username', 'first_name', 'last_name')
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(Profile, UserAdmin)