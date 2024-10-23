from django.contrib import admin
from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
import shortuuid
from userauth.models import User
from shortuuid.django_fields import ShortUUIDField
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

# Create your models here.

HOTEL_STATUS = (
    ("Draft", "Draft"),
    ("Disabled", "Disabled"),
    ("Rejected", "Rejected"),
    ("In Review", "In Review"),
    ("Live", "Live"),
)

ICON_TYPE = (
    ("bootstrap Icons", "bootstrap Icons"),
    ("Fontawsome Icons", "Fontawsome Icons"),
    ("Box Icons", "Box Icons"),
    ("Remi Icons", "Remi Icons"),
    ("Flat Icons", "Flat Icons"),
)

PAYMENT_STATUS = (
    ("Paid", "Paid"),
    ("Pending", "Pending"),
    ("Processing", "Processing"),
    ("Cancelled", "Cancelled"),
    ("Initiated", "Initiated"),
    ("Failed", "Failed"),
    ("Refunding", "Refunding"),
    ("Refunded", "Refunded"),
    ("Unpaid", "Unpaid"),
    ("Expired", "Expired"),
)

class Hotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = CKEditor5Field(null=True, blank=True, config_name='extends')
    image = models.ImageField(upload_to="hotel_gallery")
    address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    status = models.CharField(max_length=20, choices=HOTEL_STATUS, default="Live")

    tags = TaggableManager(blank=True)
    views = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    hid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmopqrstuvwxyz")
    slug = models.SlugField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            self.slug = slugify(self.name) + '-' + str(uniqueid.lower())
        super(Hotel,self).save(*args, **kwargs)

    def thumbnail(self):
        return mark_safe("<img src='%s' width='50' height='50' style='object-fit: cover; border-radius:6px;'/>" % self.image.url)
    thumbnail.short_description = 'Thumbnail'
    
    def hotel_gallery(self):
        return HotelGallery.objects.filter(hotel=self)
    
    def hotel_room_types(self):
        return RoomType.objects.filter(hotel=self)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.hotel.name}"

class HotelGallery(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to="hotel_gallery")
    hgid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmopqrstuvwxyz")

    def __str__(self):
        return str(self.hotel.name)
    
    class Meta:
        verbose_name_plural = "Hotel Gallery"

class HotelFeatures(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='features')
    icon_type = models.CharField(max_length=100, null=True, blank=True, choices=ICON_TYPE)
    icon = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Hotel Features"


class HotelFaqs(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='faqs')
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question)
    
    class Meta:
        verbose_name_plural = "Hotel FAQs"

class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='room_types')
    type = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    number_of_beds = models.PositiveIntegerField(default=0)
    room_capacity = models.PositiveIntegerField(default=0)
    rtid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmopqrstuvwxyz")
    slug = models.SlugField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.hotel.name} - {self.price}"
    
    class Meta:
        verbose_name_plural = "Hotel Room Type"


    def rooms_count(self):
        Room.objects.filter(room_type=self).count()  

    def save(self, *args, **kwargs):
        if not self.slug:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            self.slug = slugify(self.name) + '-' + str(uniqueid.lower())

        super(RoomType, self).save(*args, **kwargs)
  
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number =models.CharField(max_length=10000)
    is_available = models.BooleanField(default=True)
    rtid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmopqrstuvwxyz")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_type.type} - {self.hotel.name}"
    
    class Meta:
        verbose_name_plural = "Hotel Rooms"

    def price(self):
        return self.room_type.price 

    def number_of_beds(self):
        return self.room_type.number_of_beds
    




class OpenRooms(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    available_rooms = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type} ({self.date_created})"

class Booking(models.Model):   
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)   
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS) 
    full_name = models.CharField(max_length=1000)
    email = models.EmailField(max_length=1000)
    phone = models.CharField(max_length=100)

    hotel = models.ForeignKey(Hotel,  on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    room_type = models.ForeignKey(RoomType,  on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ManyToManyField(Room, related_name='bookings')
    before_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    check_in_date = models.DateField()
    check_out_date = models.DateField()

    total_days = models.PositiveIntegerField(default=0)
    number_of_adults= models.PositiveIntegerField(default=1)
    number_of_children= models.PositiveIntegerField(default=0)

    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    checked_in_tracker = models.BooleanField(default=False)
    checked_out_tracker = models.BooleanField(default=False)

    
    date = models.DateTimeField(auto_now_add=True)
    strip_payment_intent = models.CharField(max_length=1000, null=True, blank=True)
    success_id = models.CharField(max_length=1000, null=True, blank=True)
    booking_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmopqrstuvwxyz")

    def __str__(self):
        return f"{self.booking_id}"
    
    def rooms(self):
        return self.room.all().count()
    
# models.py

class RoomPrice(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=50)
    number_of_guest = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type} ({self.number_of_guest})"

    
class ActivityLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)  
    guest_out =models.DateTimeField() 
    guest_in =models.DateTimeField() 
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking}"
    
class StaffOnDuty(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE) 
    staff_id = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff_id}"


    

        














    

    
            


    