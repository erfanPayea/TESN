from django.db import models

from project.user import models as user_models


class City(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)


class Attraction(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    city = models.ForeignKey(City, on_delete=models.SET_NULL)
    path = models.CharField(max_length=50)


class Post(models.Model):
    owner = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, null=True, on_delete=models.SET_NULL)
    sent_time = models.DateTimeField(auto_now=True)
    file_path = models.CharField(max_length=50, null=True)
    caption = models.CharField(max_length=500)
    number_of_likes = models.PositiveIntegerField()


class Review(Post):
    attraction = models.ForeignKey(Attraction, null=False, on_delete=models.CASCADE)


class Comment(models.Model):
    owner = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    destination_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    sent_time = models.DateTimeField(auto_now=True)
    number_of_likes = models.PositiveIntegerField()


class LikePost(models.Model):
    owner = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    destination_post = models.ForeignKey(Post, on_delete=models.CASCADE)


class LikeComment(models.Model):
    owner = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    destination_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
