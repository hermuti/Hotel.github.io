from django import forms
from .models import *

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'image', 'address', 'mobile', 'email', 'status', 'tags', 'featured']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class HotelGalleryForm(forms.ModelForm):
    class Meta:
        model = HotelGallery
        fields = ['hotel','image']
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

class HotelFaqsForm(forms.ModelForm):
    class Meta:
        model = HotelFaqs
        fields = '__all__'
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control'}),
        }

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = '__all__'
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
            'number_of_beds': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'room_capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class RoomPriceForm(forms.ModelForm):
    class Meta:
        model = RoomPrice
        fields = '__all__'
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_guest': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
        }

class ActivityLogForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = '__all__'
        widgets = {
            'booking': forms.Select(attrs={'class': 'form-control'}),
            'guest_out': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'guest_in': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class StaffOnDutyForm(forms.ModelForm):
    class Meta:
        model = StaffOnDuty
        fields = '__all__'
        widgets = {
            'booking': forms.Select(attrs={'class': 'form-control'}),
            'staff_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
