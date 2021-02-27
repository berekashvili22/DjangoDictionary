from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='profile_pictures', default='default.png')

