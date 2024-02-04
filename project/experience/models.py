from django.db import models

from user import models as user_models


def upload_to_posts(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


def upload_to_attractions(instance, filename):
    return 'attractions/{filename}'.format(filename=filename)


class City(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)


class Attraction(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL, related_name="attractions")
    path = models.CharField(max_length=150)
    image = models.ImageField(upload_to=upload_to_attractions, blank=True, null=True)


class Experience(models.Model):
    owner = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="posts")
    attraction = models.ForeignKey(Attraction, null=True, on_delete=models.SET_NULL)
    sent_time = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=upload_to_posts, blank=True, null=True)
    caption = models.CharField(max_length=500)
    number_of_likes = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


class Post(Experience):
    pass


class Review(Experience):
    owner = models.ForeignKey(user_models.User, null=True, on_delete=models.SET_NULL, related_name='reviews')
    rating = models.PositiveIntegerField()
    attraction = models.ForeignKey(Attraction, null=False, on_delete=models.CASCADE, related_name="reviews")


class Comment(models.Model):
    message = models.TextField(max_length=500)
    owner = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    destination_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    sent_time = models.DateTimeField(auto_now=True)
    number_of_likes = models.PositiveIntegerField(default=0)


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
