from django.urls import path

from apps.profiles.views import ProfileView, ShippingAddressesView

urlpatterns = [
    path('', ProfileView.as_view()),
    path("shipping_addresses/", ShippingAddressesView.as_view()),
]