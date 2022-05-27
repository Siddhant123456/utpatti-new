from django.contrib import admin
from .models import Account,FarmerProfile,UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email' , 'username' , 'first_name' , 'is_active', 'date_joined')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account ,AccountAdmin)



    


admin.site.register(FarmerProfile)
admin.site.register(UserProfile)
