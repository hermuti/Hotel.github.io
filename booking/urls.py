from django.urls import path
from booking import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "booking"

urlpatterns=[
  path("check_room_availability/", views.check_room_availability, name="check_room_availability"),
  path("add_to_selection/", views.add_to_selection, name="add_to_selection"),
  path("delete_selection/", views.delete_selection, name="delete_selection"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
