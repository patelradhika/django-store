from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="user_profile", default="user_profile/default_pic.png")