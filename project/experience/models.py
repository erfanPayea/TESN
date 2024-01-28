from django.db import models

from user import models as user_models


class City(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)


class Attraction(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL, related_name="attractions")
    path = models.CharField(max_length=50)


class Experience(models.Model):
    owner = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="posts")
    attraction = models.ForeignKey(Attraction, null=True, on_delete=models.SET_NULL)
    sent_time = models.DateTimeField(auto_now=True)
    file_path = models.CharField(max_length=50, null=True)
    caption = models.CharField(max_length=500)
    number_of_likes = models.PositiveIntegerField()

    class Meta:
        abstract = True


class Post(Experience):
    pass


class Review(Experience):
    owner = models.ForeignKey(user_models.User, null=True, on_delete=models.SET_NULL)
    attraction = models.ForeignKey(Attraction, null=False, on_delete=models.CASCADE, related_name="reviews")


class Comment(models.Model):
    owner = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    destination_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    sent_time = models.DateTimeField(auto_now=True)
    number_of_likes = models.PositiveIntegerField()


class Like(models.Model):
    owner = models.ForeignKey(user_models.User, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class LikePost(Like):
    destination_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")


class LikeReview(Like):
    destination_review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="likes")


class LikeComment(Like):
    destination_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")


class CityFollowings(models.Model):
    follower = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    following = models.ForeignKey(City, on_delete=models.CASCADE)
    following_date = models.DateField(auto_now=True)
