from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from hijack_admin.admin import HijackUserAdminMixin

from customuser.models import CustomUser


def set_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


set_active.short_description = "Set is_active=True to customuser(s)"


class CustomUserAdmin(UserAdmin, HijackUserAdminMixin):
    # form = CustomUserChangeForm
    # add_form = CustomUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'hijack_field',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'telephone', 'id_card', 'accountant', 'simulation')}),
        (_('Companies'), {'fields': ('companies',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)
    filter_horizontal = ('companies',)
    actions = [set_active]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
