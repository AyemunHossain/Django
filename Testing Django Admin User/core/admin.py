from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import Account
from django.utils.translation import gettext as _


class AccountAdmin(UserAdmin):
    ordering = ['id']
    list_display = ['email']
    readonly_fields = ('date_joined','last_login')
    fieldsets = (
        (_("User Details"), {'fields': ('email', )}),
        (_("Account Details"), {'fields': ('date_joined', 'last_login')}),
        (_("Permission"), {'fields': ('is_active', 'is_staff', 'is_admin')}),
    )
    add_fieldsets = (
    ("User Details", {'fields': ('email', 'password1', 'password2')}),
    ("Permission", {'fields': ('is_active', 'is_staff', 'is_admin')}),
)

admin.site.register(Account, AccountAdmin)
