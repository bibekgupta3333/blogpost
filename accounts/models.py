from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from .validators import (validate_phone_number,)
import uuid
# Create your models here.


def image_path(_, filename):
    extension = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex
    new_file_name = unique_id+'.'+extension
    new_file_name = f"{_.created}/{_.user}/{new_file_name}"
    print(new_file_name)
    return "users/"+new_file_name


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=14,
                             validators=[validate_phone_number, ], blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(
        upload_to=image_path, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
