from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class AccountAdmin(UserAdmin):
    ordering = ['id']
    list_display = ['email']
    readonly_fields = ('date_joined','last_login')
    fieldsets = (
        (_("User Details"), {'fields': ('email', 'password')}),
        (_("Account Details"), {'fields': ('date_joined', 'last_login')}),
        (_("Permission"), {'fields': ('is_active', 'is_staff', 'is_admin')}),
    )
    add_fieldsets = (
    ("User Details", {'fields': ('email', 'password1', 'password2')}),
    ("Permission", {'fields': ('is_active', 'is_staff', 'is_admin')}),
)

admin.site.register(get_user_model(), AccountAdmin)
