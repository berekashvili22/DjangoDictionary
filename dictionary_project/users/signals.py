from django.contrib.auth.models import User
from django.db.models.signals import post_save

from . models import Profile

def user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
        )
        print('profile was created')

post_save.connect(user_profile, sender=User)