from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("book/", views.create_booking, name="create_booking"),
    path("payment/<int:booking_id>/", views.payment, name="payment"),
    path("contact/", views.contact, name="contact"),
]
