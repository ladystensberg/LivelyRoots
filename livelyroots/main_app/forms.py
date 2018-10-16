from django.forms import ModelForm, Form, CharField, PasswordInput, EmailField, Textarea, TextInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Family, User

class ContactForm(Form):
    email = EmailField()
    message = CharField(
        max_length=2000,
        widget=Textarea()
    )

class LoginForm(Form):
    username = CharField(label="username", max_length=64)
    password = CharField(widget=PasswordInput())

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].help_text = ''

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class JoinFamily(Form):
    family_code = CharField(max_length=2000)