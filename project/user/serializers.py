from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
from . import models

class Fallowing(ModelSerializer):
    class Meta:
        models = models.Followers
        fields = '__all__'


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