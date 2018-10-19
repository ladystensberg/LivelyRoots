from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .forms import ContactForm, LoginForm, SignUpForm, JoinFamily, PostForm, CommentForm, ProfileForm
from .models import Family, Member, Post, Comment
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
        username = self.request.user.username
        self.object = form.save(commit=True)
        family = Family.objects.get(id=self.object.id)
        family.users.add(user)
        form.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))

@method_decorator(login_required, name='dispatch')
class UpdatePost(UpdateView):
    model = Post
    fields = ['content']

@method_decorator(login_required, name='dispatch')
class UpdateComment(UpdateView):
    model = Comment
    fields = ['content']

@method_decorator(login_required, name='dispatch')
class UpdateUser(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']

    success_url = '/'

@login_required(login_url='/login/')
def join_family(request):
    if request.method == 'POST':
        form = JoinFamily(request.POST)
        if form.is_valid():
            family_code = form.cleaned_data['family_code']
            user = request.user
            family = Family.objects.get(family_code=family_code)
            family.users.add(user)
            return HttpResponseRedirect(reverse('profile', kwargs={'username': user}))
    else:
        form = JoinFamily()
    return render(request, 'join_family.html', {'form': form})

@login_required(login_url='/login/')
def remove_family(request, family_id):
    username = request.user.username
    if username == request.user.username:
        family = Family.objects.get(id=family_id)
        user = request.user
        family.users.remove(user)
        return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))

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
                    return HttpResponseRedirect('/posts')
                else:
                    form = LoginForm()
                    errMsg = "This account has been disabled. Please contact support for assistance."
                    return render(request, 'login.html', {'form': form, 'err': errMsg})
            else:
                form = LoginForm()
                errMsg = "Your username and/or password is incorrect. Please try again."
                return render(request, 'login.html', {'form': form, 'err': errMsg})
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
            return HttpResponseRedirect('/posts')
        else:
            form = SignUpForm()
            errMsg = "One or more fields was invalid, please try again."
            return render(request, 'signup.html', {'form': form, 'err': errMsg})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

@login_required(login_url='/login/')
def profile(request, username):
    if username == request.user.username:
        user = User.objects.get(username=username)
        members = Member.objects.filter(user_id=user)
        families = Family.objects.filter(users=user)
        return render(request, 'profile.html', {'username': username, 'families': families, 'members': members})
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def edit_profile(request, username):
    if username == request.user.username:
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user_id = request.user.id
                profile.save()
            return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))
        else:
            form = ProfileForm()
            return render(request, 'user/edit_profile.html', {'username': username, 'form':form})

@login_required(login_url='/login/')
def delete_user(request, username):
    if username == request.user.username:
        user = User.objects.get(username=username)
        user.delete()
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def delete_user_confirm(request, username):
    username = request.user.username
    return render(request, 'user/delete_user_confirm.html', {'username': username})


@login_required(login_url='/login/')
def post_feed(request):
    returned_posts = []
    family_members = []
    user = request.user.id
    user_families = request.user.family_set.all()
    if user_families.count() == 0:
        error = True
        return render(request, 'posts/index.html', {'error': error})
    else:
        create_post_form = PostForm()
        for family in user_families:
            for user in family.users.all():
                if user not in family_members:
                    family_members.append(user)
                posts = user.post_set.all()
                for post in posts:
                    if post not in returned_posts:
                        returned_posts.append(post)
        return render(request, 'posts/index.html', {'user': user, 'returned_posts': returned_posts, 'family_members': family_members})

@login_required(login_url='/login/')
def user_posts(request, username):
    create_post_form = PostForm()
    user = User.objects.get(username=username)
    posts = user.post_set.all()
    if posts.count() == 0 and request.user.username != username:
        error = True
        return render(request, 'user/user_posts.html', {'username':username, 'error':error})
    return render(request, 'user/user_posts.html', {'username': username, 'posts': posts, 'create_post_form': create_post_form})

@login_required(login_url='/login/')
def create_post(request):
    form = PostForm(request.POST)
    username = request.user.username
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.user_id = request.user.id
        new_post.save()
    return HttpResponseRedirect(reverse('user_posts', kwargs={'username': username}))

@login_required(login_url='/login/')
def view_post(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post_id=post_id)
    add_comment_form = CommentForm()
    return render(request, 'posts/detail.html', {
    	'post': post, 'comments': comments, 'add_comment_form': add_comment_form
    })

@login_required(login_url='/login/')
def delete_post(request, post_id):
    username = request.user.username
    if username == request.user.username:
        post = Post.objects.get(id=post_id)
        post.delete()
        return HttpResponseRedirect(reverse('user_posts', kwargs={'username': username}))

@login_required(login_url='/login/')
def delete_post_confirm(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/delete_post_confirm.html', {'post': post})

@login_required(login_url='/login/')
def add_comment(request, post_id):
    form = CommentForm(request.POST)
    post = Post.objects.get(id=post_id)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user_id = request.user.id
        new_comment.post_id = post_id
        new_comment.save()
    return HttpResponseRedirect(reverse('view_post', kwargs={'post_id': post_id}))

@login_required(login_url='/login/')
def delete_comment(request, post_id, comment_id):
    username = request.user.username
    if username == request.user.username:
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return HttpResponseRedirect(reverse('view_post', kwargs={'post_id': post_id}))

@login_required(login_url='/login/')
def delete_comment_confirm(request, post_id, comment_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    return render(request, 'posts/delete_comment_confirm.html', {'post': post, 'comment': comment})