from django.contrib import admin
from userauth.models import User,profile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'username']
    list_display = ['username', 'full_name', 'email', 'phone','gender']


class profileAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'user__username']
    list_display = [ 'full_name','user', 'verified']




admin.site.register(User, UserAdmin)
admin.site.register(profile, profileAdmin)
