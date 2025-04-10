from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Import your custom User model
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    # Add the custom field to the fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_customer'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_customer'),
        }),
    )

    list_display = ('username', 'email', 'is_staff', 'is_customer')
    search_fields = ('username', 'email')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
