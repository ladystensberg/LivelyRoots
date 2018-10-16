from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ContactForm, LoginForm, SignUpForm, JoinFamily
from .models import Family, Member
from django.core.mail import send_mail
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class FamilyCreate(CreateView):
    model = Family
    fields = ['family_name']

    def form_valid(self, form):
        user = self.request.user.id
        self.object = form.save(commit=True)
        family = Family.objects.get(id=self.object.id)
        family.members.add(user)
        form.save()
        return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def join_family(request):
    if request.method == 'POST':
        form = JoinFamily(request.POST)
        if form.is_valid():
            family_code = form.cleaned_data['family_code']
            user = request.user
            family = Family.objects.get(family_code=family_code)
            family.members.add(user)
            return HttpResponseRedirect('/')
    else:
        form = JoinFamily()
    return render(request, 'join_family.html', {'form': form})

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
        return HttpResponseRedirect('/contact/sent')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def contact_sent(request):
    return render(request, 'contact_sent.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
                    return HttpResponseRedirect('/')
            else:
                print("The username and/or password is incorrect.")
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

@login_required(login_url='/login/')
def profile(request, username):
    if username == request.user.username:
        user = User.objects.get(username=username)
        members = Member.objects.filter(member_id=user)
        families = Family.objects.filter(members=user)
        return render(request, 'profile.html', {'username': username, 'families': families, 'members': members})
    else:
        return HttpResponseRedirect('/')

