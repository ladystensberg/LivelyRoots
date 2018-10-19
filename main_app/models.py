from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid

class Family(models.Model):
    def get_family_code():
        return uuid.uuid4()

    family_name = models.CharField(max_length=50)
    family_code = models.UUIDField(max_length=10, default = get_family_code, editable=False)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f"Family Name: {self.family_name}, Family Code: {self.family_code}"
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.user.id})

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return f"{self.user.username}'s birthday is {self.birth_date}. Location is {self.location}."

    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.user.id})

class Post(models.Model):
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}. {self.content}. {self.user.username}"

    def get_absolute_url(self):
        return reverse('view_post', kwargs={'post_id': self.id})

class Comment(models.Model):
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}. {self.content}. {self.post}. {self.user.username}"

    def get_absolute_url(self):
        return reverse('view_post', kwargs={'post_id': self.post.id})