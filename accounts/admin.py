from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import account,UserProfile

# Register your models here.

class  accountAdmin(UserAdmin):
    list_display=('email','first_name','last_name','username','last_login','Date_joined','is_active')
    list_display_links = ('email','first_name','last_name','username')
    readonly_fields = ('Date_joined','last_login')
    ordering = ('-Date_joined',)


    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(account, accountAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','image_tag')

admin.site.register(UserProfile, UserProfileAdmin )
