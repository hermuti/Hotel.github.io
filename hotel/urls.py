from django.urls import path,include
from hotel import views

app_name = "hotel"

urlpatterns=[
  path("",views.index,name="index"),
  path("hotel/", views.hotel, name="hotel"),
  path("detail/<slug>/", views.hotel_detail, name="hotel_detail"),
  path("detail/<slug:slug>/room_type/<slug:rt_slug>/", views.room_type_detail, name="room_type_detail"),
  path("selected_rooms/", views.selected_rooms, name="selected_rooms"),
  path("checkout/<booking_id>/", views.checkout, name="checkout"),


  path("service/",views.service,name="service"),
  path("contact/",views.contact,name="contact"),
  path("about/",views.about,name="about"),


 

  path('hotel/<slug:slug>/delete/', views.hotel_delete_view, name='hotel_delete'),
  path('hotel/<int:pk>/update/', views.hotel_update, name='hotel_update'),
  path("add_hotel/", views.add_hotel, name="add_hotel"),
  



   
]




