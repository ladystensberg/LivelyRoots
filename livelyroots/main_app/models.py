from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Family(models.Model):
    def get_family_code():
        return uuid.uuid4()

    family_name = models.CharField(max_length=50)
    family_code = models.UUIDField(max_length=10, default = get_family_code, editable=False)
    
    def __str__(self):
        return f"Family Name: {self.family_name}, Family Code: {self.family_code}"
