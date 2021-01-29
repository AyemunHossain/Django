from django.contrib import admin
from .models import Account, ProfileFeedItem
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
	list_display = ('email','username','date_joined','last_login','is_admin','is_active','is_staff')
	search_fields = ['email','username',]
	readonly_fields = ('date_joined','last_login')
	list_display_links = ('email','username',)

	filter_horizontal = ()
	list_filter = ('is_admin','is_staff','is_active')
	fieldsets =(
			
			("User Details",{'fields':('username','email')}),
			("Account Details",{'fields':('date_joined','last_login')}),
			("Permission",{'fields':('is_active','is_staff','is_admin')}),
		)

	add_fieldsets=(
			
			("User Details",{'fields':('username','email','password1','password2')}),
			("Permission",{'fields':('is_active','is_staff','is_admin')}),
		
		)
admin.site.register(Account, AccountAdmin)
admin.site.register(ProfileFeedItem)
