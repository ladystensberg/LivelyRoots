from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea()
    )