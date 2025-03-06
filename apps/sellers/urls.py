from django.urls import path

from apps.sellers.views import SellersView, ProductsBySellerView

urlpatterns = [
    path("", SellersView.as_view()),
    path("products/", ProductsBySellerView.as_view()),
]