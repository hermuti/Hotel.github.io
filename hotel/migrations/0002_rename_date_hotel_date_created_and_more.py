# Generated by Django 5.0.1 on 2024-03-22 14:38

import django.db.models.deletion
import django_ckeditor_5.fields
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotel',
            old_name='date',
            new_name='date_created',
        ),
        migrations.AlterField(
            model_name='hotel',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='image',
            field=models.ImageField(upload_to='hotel_gallery'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Processing', 'Processing'), ('Cancelled', 'Cancelled'), ('Initiated', 'Initiated'), ('Failed', 'Failed'), ('Refunding', 'Refunding'), ('Refunded', 'Refunded'), ('Unpaid', 'Unpaid'), ('Expired', 'Expired')], max_length=100)),
                ('full_name', models.CharField(max_length=1000)),
                ('email', models.EmailField(max_length=1000)),
                ('phone', models.CharField(max_length=100)),
                ('before_discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('saved', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('total_days', models.PositiveIntegerField(default=0)),
                ('number_of_adults', models.PositiveIntegerField(default=1)),
                ('number_of_children', models.PositiveIntegerField(default=0)),
                ('checked_in', models.BooleanField(default=False)),
                ('checked_out', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('checked_in_tracker', models.BooleanField(default=False)),
                ('checked_out_tracker', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('strip_payment_intent', models.CharField(blank=True, max_length=1000, null=True)),
                ('success_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('booking_id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmopqrstuvwxyz', length=10, max_length=20, prefix='', unique=True)),
                ('hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='hotel.hotel')),
                ('room_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel.hotel')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_out', models.DateTimeField()),
                ('guest_in', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.booking')),
            ],
        ),
        migrations.CreateModel(
            name='HotelFaqs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1000)),
                ('answer', models.CharField(blank=True, max_length=1000, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faqs', to='hotel.hotel')),
            ],
            options={
                'verbose_name_plural': 'Hotel FAQs',
            },
        ),
        migrations.CreateModel(
            name='HotelFeatures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon_type', models.CharField(blank=True, choices=[('bootstrap Icons', 'bootstrap Icons'), ('Fontawsome Icons', 'Fontawsome Icons'), ('Box Icons', 'Box Icons'), ('Remi Icons', 'Remi Icons'), ('Flat Icons', 'Flat Icons')], max_length=100, null=True)),
                ('icon', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='hotel.hotel')),
            ],
            options={
                'verbose_name_plural': 'Hotel Features',
            },
        ),
        migrations.CreateModel(
            name='HotelGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='hotel_gallery')),
                ('hgid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmopqrstuvwxyz', length=10, max_length=20, prefix='', unique=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='hotel.hotel')),
            ],
            options={
                'verbose_name_plural': 'Hotel Gallery',
            },
        ),
        migrations.CreateModel(
            name='OpenRooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('available_rooms', models.PositiveIntegerField()),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('comment', models.TextField()),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=10000)),
                ('is_available', models.BooleanField(default=True)),
                ('rtid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmopqrstuvwxyz', length=10, max_length=20, prefix='', unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='hotel.hotel')),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
            options={
                'verbose_name_plural': 'Hotel Rooms',
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='room',
            field=models.ManyToManyField(related_name='bookings', to='hotel.room'),
        ),
        migrations.CreateModel(
            name='RoomPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(max_length=50)),
                ('number_of_guest', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=60)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('number_of_beds', models.PositiveIntegerField(default=0)),
                ('room_capacity', models.PositiveIntegerField(default=0)),
                ('rtid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmopqrstuvwxyz', length=10, max_length=20, prefix='', unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_types', to='hotel.hotel')),
            ],
            options={
                'verbose_name_plural': 'Hotel Room Type',
            },
        ),
        migrations.CreateModel(
            name='StaffOnDuty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_id', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.booking')),
            ],
        ),
    ]
