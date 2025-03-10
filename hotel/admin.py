from django.contrib import admin
from hotel.models import *


# Register your models here.

class HotelGalleryInline(admin.TabularInline):
  model = HotelGallery

class HotelAdmin(admin.ModelAdmin):
  inlines = [HotelGalleryInline]
  list_display = ['thumbnail','name','user','status']
  prepopulated_fields = {"slug":("name",)}

admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelGallery)
admin.site.register(HotelFeatures)
admin.site.register(HotelFaqs)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(ActivityLog)
admin.site.register(StaffOnDuty)

