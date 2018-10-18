from django.contrib import admin
from .models import Family, Member, Post, Comment
# Register your models here.
admin.site.register(Family)
admin.site.register(Member)
admin.site.register(Post)
admin.site.register(Comment)