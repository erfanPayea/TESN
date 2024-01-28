from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_GOLD, 'Gold'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_BRONZE, 'Bronze')
    ]
    phone = models.CharField(max_length=13)
    birth_date = models.DateField(null=True)
    date_joined = models.DateField(auto_now=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)


class Otp(models.Model):
    passkey = models.CharField(max_length=6, null=True)
    created_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Followers(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    following_date = models.DateField(auto_now=True)
