from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .emails import send_booking_confirmation
from .forms import BookingForm, ContactForm, PaymentForm
from .models import (
    Booking, PastEventPhoto, Review, SiteConfig, UpcomingEvent,
)


def home(request):
    config = SiteConfig.load()
    context = {
        "config": config,
        "upcoming_event": UpcomingEvent.objects.filter(is_active=True).first(),
        "reviews": Review.objects.filter(is_approved=True)[:12],
        "photos": PastEventPhoto.objects.filter(is_visible=True)[:16],
        "booking_form": BookingForm(),
        "contact_form": ContactForm(),
    }
    return render(request, "party/home.html", context)


def create_booking(request):
    config = SiteConfig.load()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.price = (
                config.couple_price if booking.entry_type == Booking.ENTRY_COUPLE
                else config.single_price
            )
            booking.save()
            send_booking_confirmation(booking)
            messages.success(
                request,
                "Booking received! Check your email for confirmation, then "
                "complete payment below.",
            )
            return redirect("payment", booking_id=booking.id)
        messages.error(request, "Please fix the errors in the booking form.")
        return render_home_with_errors(request, booking_form=form)
    return redirect("home")


def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    config = SiteConfig.load()
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=booking)
        if form.is_valid():
            form.save(commit=False)
            booking.payment_status = Booking.PAYMENT_SUBMITTED
            booking.save()
            messages.success(
                request,
                "Payment reference submitted. Your entry will be confirmed by the team shortly.",
            )
            return redirect("payment", booking_id=booking.id)
    else:
        form = PaymentForm(instance=booking)
    return render(request, "party/payment.html", {
        "booking": booking, "config": config, "form": form,
    })


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent! We'll get back to you soon.")
            return redirect("home")
        messages.error(request, "Please fix the errors in the contact form.")
        return render_home_with_errors(request, contact_form=form)
    return redirect("home")


def render_home_with_errors(request, booking_form=None, contact_form=None):
    config = SiteConfig.load()
    context = {
        "config": config,
        "upcoming_event": UpcomingEvent.objects.filter(is_active=True).first(),
        "reviews": Review.objects.filter(is_approved=True)[:12],
        "photos": PastEventPhoto.objects.filter(is_visible=True)[:16],
        "booking_form": booking_form or BookingForm(),
        "contact_form": contact_form or ContactForm(),
    }
    return render(request, "party/home.html", context)
