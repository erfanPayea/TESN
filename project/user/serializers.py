from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
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
        data['cantact']= {
                'id': other_user.id,
                'username': other_user.username,
                # Add other user fields as needed
            }
        return data


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "email",
            "username",
            "id",
            "phone",
            "date_joined",
            "membership",
        )

# class TestApi(ModelSerializer):
#
#     class Meta:
#         model = models.test
#         fields = '__all__'
#
#     # def to_representation(self, instance):
#     #     res = super().to_representation(instance)
#     #     res["address"] = instance.address.st
#     #     return res
#
#     def validate_phone(self, value):
#         if len(value) != 11:
#             raise ValidationError("Error in phone")
#         return value
