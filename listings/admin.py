from django.contrib import admin
from .models import Developer, Property


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'developer', 'location', 'price', 'bedrooms', 'bathrooms')
    list_filter = ('location', 'bedrooms')
