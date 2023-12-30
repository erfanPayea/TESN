from rest_framework.serializers import ModelSerializer
from . import models


class Post(ModelSerializer):
    class Meta:
        models = models.Post
        fields = '__all__'


class Review(ModelSerializer):
    class Meta:
        models = models.Review
        fields = '__all__'


class LikePost(ModelSerializer):
    class Meta:
        models = models.LikePost
        fields = '__all__'


class LikeReview(ModelSerializer):
    class Meta:
        models = models.LikeReview
        fields = '__all__'


class LikeComment(ModelSerializer):
    class Meta:
        models = models.LikeComment
        fields = '__all__'
