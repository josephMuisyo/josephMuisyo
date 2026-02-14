from django.urls import path

from .views import customer_message_create, health_check, menu_list

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("menu/", menu_list, name="menu-list"),
    path("contact/", customer_message_create, name="customer-message-create"),
]
