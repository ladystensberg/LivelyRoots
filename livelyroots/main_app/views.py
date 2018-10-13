from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ContactForm
from django.core.mail import send_mail

def index(request):
    return render(request, 'index.html')

def faq(request):
    return render(request, 'faq.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail('LivelyRoots Contact Form', message, email, ['ladystensberg@gmail.com'], fail_silently=False)
        return HttpResponseRedirect('/contact/sent') ##change this to form success page
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def contact_sent(request):
    return render(request, 'contact_sent.html')