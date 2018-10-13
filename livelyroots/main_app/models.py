from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Family(models.Model):
    def get_family_code():
        return uuid.uuid4()

    family_name = models.CharField(max_length=50)
    family_code = models.UUIDField(max_length=10, default = get_family_code, editable=False)
    members = models.ManyToManyField(User)

    def __str__(self):
        return f"Family Name: {self.family_name}, Family Code: {self.family_code}"

class Member(models.Model):
    member = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return f"{self.member.username}'s birthday is {self.birth_date}. Location is {self.location}."

class Post(models.Model):
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}. {self.content}. {self.member.username}"

class Comment(models.Model):
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}. {self.content}. {self.post}. {self.member.username}"