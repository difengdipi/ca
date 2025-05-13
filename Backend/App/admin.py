from django.contrib import admin
from .models import *

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = [
        'role_name',
        'description',
        'created_at',
    ]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'password',
        'name',
        'gender',
        'avatar',
        'phone',
        'email',
        'role',
        'dept',
        'notes',
    ]

@admin.register(Canteen)
class CanteenAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'address',
        'contact_person',
        'contact_phone',
        'created_at',
    ]

@admin.register(Window)
class WindowAdmin(admin.ModelAdmin):
    list_display = [
        'canteen',
        'name',
        'description',
        'business_hours',
        'contact_person',
        'contact_phone',
        'created_at',
    ]

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = [
        'window',
        'name',
        'description',
        'price',
        'image',
        'stock_quantity',
        'time',
    ]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'address',
        'phone',
        'is_default',
        'created_at',
    ]


@admin.register(Swiper)
class SwiperAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'image',
        'location',
    ]

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'subject',
        'message',
        'resolved',
        'image',
        'video',
        'created_at',
    ]
