from django.contrib import admin

from .models import CustomerMessage, MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_kes", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")


@admin.register(CustomerMessage)
class CustomerMessageAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "phone_number", "created_at")
    search_fields = ("customer_name", "phone_number", "message")
