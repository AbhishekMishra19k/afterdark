from django import forms

from .models import Booking, ContactMessage


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "full_name", "age", "email", "phone", "location",
            "screening_answer", "entry_type",
        ]
        widgets = {
            "screening_answer": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "screening_answer": "Why do you want to attend?",
        }

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age < 18:
            raise forms.ValidationError(
                "AFTERDARK is strictly an 18+ event. You must be 18 or older to book."
            )
        return age

    def clean_entry_type(self):
        entry_type = self.cleaned_data["entry_type"]
        if entry_type not in dict(Booking.ENTRY_CHOICES):
            raise forms.ValidationError("Group bookings are not allowed. Choose Single or Couple.")
        return entry_type


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["payment_reference"]
        widgets = {
            "payment_reference": forms.TextInput(attrs={
                "placeholder": "UPI transaction ID / UTR number"
            }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }
