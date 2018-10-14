from django.forms import ModelForm, Form, CharField, PasswordInput, EmailField, Textarea

class ContactForm(Form):
    email = EmailField()
    message = CharField(
        max_length=2000,
        widget=Textarea()
    )

class LoginForm(Form):
    username = CharField(label="username", max_length=64)
    password = CharField(widget=PasswordInput())