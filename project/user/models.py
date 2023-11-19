from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here
class User(AbstractUser):
    phone = models.CharField(max_length=13)
    test = models.CharField(max_length=256)
    birth_date = models.DateField(null=True)
    date_joined = models.DateField(auto_now=True)


class Followers(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    following_date = models.DateField(auto_now=True)

# class CityFollowings(models.Model):
#     follower = models.ForeignKey(User, on_delete=models.CASCADE)
#     following = models.ForeignKey(City, on_delete=models.CASCADE)
#     following_date = models.DateField(auto_now=True)



