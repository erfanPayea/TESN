from rest_framework.serializers import ModelSerializer
from rest_framework.utils import json

from . import models


class Follower(ModelSerializer):
    class Meta:
        model = models.Followers
        fields = (
            "id",
            "following_date",
        )

    def to_representation(self, instance):
        request = self.context.get('request', None)
        current_user = getattr(request, 'user', None)
        data = super().to_representation(instance)
        if instance.follower == current_user:
            other_user = instance.following
        elif instance.following == current_user:
            other_user = instance.follower
        else:
            return data
        data['cantact'] = {
            'id': other_user.id,
            'username': other_user.username,
            'avatarImage': "http://127.0.0.1:8000/media/" + str(other_user.avatar_image)
            # Add other user fields as needed
        }
        return data


def user_serializer(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "dateJoined": user.date_joined,
        "membership": user.membership,
        "avatarImage": "http://127.0.0.1:8000/media/" + str(user.avatar_image)
    }
