from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from hotel.models import *
from datetime import datetime

from hotel.forms import *


def index(request):
    hotels = Hotel.objects.filter(status="Live")
    context = {"hotels": hotels}
    return render(request, "hotel/hotel.html", context)

def hotel_detail(request, slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    context = {"hotel": hotel}
    return render(request, "hotel/hotel_detail.html", context)

def room_type_detail(request, slug, rt_slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    room_type = RoomType.objects.get(hotel=hotel, slug=rt_slug)
    rooms = Room.objects.filter(room_type=room_type, is_available=True)

    id = request.GET.get("hotel-id")
    checkin = request.GET.get("checkin")
    checkout = request.GET.get("checkout")
    adult = request.GET.get("adult")
    children = request.GET.get("children")

    context = {
        "hotel": hotel,
        "room_type": room_type,
        "rooms": rooms,
        "checkin": checkin,
        "checkout": checkout,
        "adult": adult,
        "children": children,
    }

    return render(request, "hotel/room_type_detail.html", context)
#booking system starts here
def selected_rooms(request):
    total = 0
    room_count = 0
    total_days = 0
    adult = 0
    children = 0
    checkin = ""
    checkout = ""
    room_type = None
    hotel = None

    if 'selection_data_obj' in request.session:
        if request.method == "POST":
            for h_id, item in request.session['selection_data_obj'].items():
                id = int(item['hotel_id'])
                checkin = item['checkin']
                checkout = item['checkout']
                adult = int(item['adult'])
                room_type_id = int(item['room_type'])
                room_id = int(item['room_id'])

                hotel = Hotel.objects.get(id=id)
                room = Room.objects.get(id=room_id)
                room_type = RoomType.objects.get(id=room_type_id)

                if checkin and checkout:
                    checkin_date = datetime.strptime(checkin, "%Y-%m-%d")
                    checkout_date = datetime.strptime(checkout, "%Y-%m-%d")
                    time_difference = checkout_date - checkin_date
                    total_days = time_difference.days

                full_name = request.POST.get('full_name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')

                booking = Booking.objects.create(
                    hotel=hotel,
                    room_type=room_type,
                    check_in_date=checkin,
                    check_out_date=checkout,
                    total_days=total_days,
                    number_of_adults=adult,
                    number_of_children=children,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    user=request.user if request.user.is_authenticated else None
                )

                for h_id, item in request.session['selection_data_obj'].items():
                    room_id = int(item["room_id"])
                    room = Room.objects.get(id=room_id)
                    booking.room.set([room])

                    room_count += 1
                    days = total_days
                    price = room_type.price 
                    room_price = price * room_count
                    total = room_price * days

                    booking.total += float(total)
                    booking.before_discount += float(total)
                    booking.save()

                    messages.success(request, "Checkout Now")
                    return redirect("hotel:checkout", booking.booking_id)

    hotel = None
    for h_id, item in request.session['selection_data_obj'].items():
        id = int(item['hotel_id'])
        checkin = item['checkin']
        checkout = item['checkout']
        adult = int(item['adult'])
        room_type_id = int(item['room_type'])
        room_id = int(item['room_id'])

        room_type = RoomType.objects.get(id=room_type_id)

        date_format = "%Y-%m-%d"
        checkin_date = datetime.strptime(checkin, date_format)
        checkout_date = datetime.strptime(checkout, date_format)
        time_difference = checkout_date - checkin_date
        total_days = time_difference.days

        room_count += 1
        days = total_days
        price = room_type.price

        room_price = price * room_count
        total = room_price * days

        hotel = Hotel.objects.get(id=id)

    context = {
        "data": request.session['selection_data_obj'],
        "total_selected_items": len(request.session['selection_data_obj']),
        "total": total,
        "total_days": total_days,
        "adult": adult,
        "children": children,
        "checkin": checkin,
        "checkout": checkout,
        "hotel": hotel,
    }

    return render(request, "hotel/selected_rooms.html", context)

# This focuses on checkout
def checkout(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    context = {"booking": booking}
    return render(request, "hotel/checkout.html", context)

def hotel(request):
    return render(request, "hotel/hotel.html")

def service(request):
    return render(request, "hotel/service.html")

def about(request):
    return render(request, "hotel/about.html")

def contact(request):
    return render(request, "hotel/contact.html")




#delete hotel

def hotel_delete_view(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    if request.method == 'POST':
        hotel.delete()
        return redirect('hotel_list') 

  
    return render(request, 'hotel_confirm_delete.html', {'hotel': hotel})





#updat hotel

def hotel_update(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('hotel_detail', slug=hotel.slug)
    else:
        form = HotelForm(instance=hotel)

    return render(request, 'hotel/hotel_update.html', {'form': form})

#add_hotel
def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hotel_detail')  # Redirect to hotel detail with the new hotel's pk
    else:
        form = HotelForm()
    return render(request, "hotel/add_hotel.html", {'form': form})




from django.shortcuts import render, redirect
from .forms import *

def modify_hotel(request, pk):
    if request.method == 'POST':
        hotel_form = HotelForm(request.POST, request.FILES)
        hotel_gallery_form = HotelGalleryForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        hotel_faqs_form = HotelFaqsForm(request.POST)
        room_type_form = RoomTypeForm(request.POST)
        room_form = RoomForm(request.POST)
        room_price_form = RoomPriceForm(request.POST)
        activity_log_form = ActivityLogForm(request.POST)
        staff_on_duty_form = StaffOnDutyForm(request.POST)

        if all(form.is_valid() for form in [hotel_form, hotel_gallery_form, review_form, hotel_faqs_form, room_type_form, room_form, room_price_form, activity_log_form, staff_on_duty_form]):
            hotel = hotel_form.save()
            hotel_gallery_form.instance.hotel = hotel
            hotel_gallery_form.save()
            review_form.instance.hotel = hotel
            review_form.save()
            hotel_faqs_form.instance.hotel = hotel
            hotel_faqs_form.save()
            room_type_form.instance.hotel = hotel
            room_type_form.save()
            room_form.instance.hotel = hotel
            room_form.save()
            room_price_form.instance.hotel = hotel
            room_price_form.save()
            activity_log_form.instance.booking = hotel.bookings.first()  # Assuming bookings are related to hotel
            activity_log_form.save()
            staff_on_duty_form.instance.booking = hotel.bookings.first()  # Assuming bookings are related to hotel
            staff_on_duty_form.save()

            # Redirect or render success page
            return redirect('hotel_detail', slug=hotel.slug)
    else:
        hotel_form = HotelForm()
        hotel_gallery_form = HotelGalleryForm()
        review_form = ReviewForm()
        hotel_faqs_form = HotelFaqsForm()
        room_type_form = RoomTypeForm()
        room_form = RoomForm()
        room_price_form = RoomPriceForm()
        activity_log_form = ActivityLogForm()
        staff_on_duty_form = StaffOnDutyForm()
        
    return render(request, 'modify_hotel.html', {
        'hotel_form': hotel_form,
        'hotel_gallery_form': hotel_gallery_form,
        'review_form': review_form,
        'hotel_faqs_form': hotel_faqs_form,
        'room_type_form': room_type_form,
        'room_form': room_form,
        'room_price_form': room_price_form,
        'activity_log_form': activity_log_form,
        'staff_on_duty_form': staff_on_duty_form,
    })
