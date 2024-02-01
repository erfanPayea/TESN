import datetime
import sys

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user import models as user_models

from . import models as experience_models
from . import serializers, errors
from user import errors as user_errors


class Posts(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            attraction_id = request.data["attractionId"]
            caption = request.data["caption"]
            file_path = request.data["filePath"]
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))

        attraction = experience_models.Attraction.objects.filter(id=attraction_id).first()
        if attraction is None and attraction_id != "-1":
            return Response(errors.ATTRACTION_NOT_FOUND.get("data"), errors.ATTRACTION_NOT_FOUND.get("status"))

        max_post_per_day = sys.maxsize
        if request.user.membership == 'B':
            max_post_per_day = 5
        elif request.user.membership == 'S':
            max_post_per_day = 10
        today_posts = len(
            experience_models.Post.objects.filter(owner=request.user, sent_time__day=datetime.date.today().day))
        if today_posts >= max_post_per_day:
            return Response(errors.LIMIT_REACHED.get("data"), errors.LIMIT_REACHED.get("status"))

        new_post = experience_models.Post(owner=request.user, attraction=attraction, caption=caption,
                                          file_path=file_path)
        new_post.save()
        return Response({}, status.HTTP_200_OK)


class Reviews(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            rating = int(request["rating"])
            attraction_id = request.data["attractionId"]
            caption = request.data["caption"]
            file_path = request.data["filePath"]
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))

        attraction = experience_models.Attraction.objects.filter(id=attraction_id)
        if attraction is None:
            return Response(errors.ATTRACTION_NOT_FOUND.get("data"), errors.ATTRACTION_NOT_FOUND.get("status"))

        max_review_per_day = 5
        if request.user.membership == 'B':
            max_review_per_day = 2
        elif request.user.membership == 'S':
            max_review_per_day = 0
        today_reviews = len(
            experience_models.Review.objects.filter(owner=request.user, sent_time__day=datetime.date.today().day))
        if today_reviews >= max_review_per_day:
            return Response(errors.LIMIT_REACHED.get("data"), errors.LIMIT_REACHED.get("status"))

        new_review = experience_models.Review(owner=request.user, attraction=attraction,
                                              caption=caption, file_path=file_path, rating=rating)
        new_review.save()
        return Response({}, status.HTTP_200_OK)


class Likes(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.data)
        try:
            destination_type = request.data["destinationType"]
            destination_id = int(request.data["destinationId"])
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))

        if destination_type == "POST":
            destination_post = experience_models.Post.objects.filter(id=destination_id).first()
            if destination_post is None:
                return Response(errors.POST_NOT_FOUND.get("data"), errors.POST_NOT_FOUND.get("status"))
            like_post = experience_models.LikePost.objects.filter(destination_post=destination_post,
                                                                  owner=request.user).first()
            if like_post is None:
                destination_post.number_of_likes += 1
                new_like_post = experience_models.LikePost(owner=request.user, destination_post=destination_post)
                new_like_post.save()

            else:
                destination_post.number_of_likes -= 1
                like_post.delete()

            destination_post.save()

        elif destination_type == "REVIEW":
            destination_review = experience_models.Review.objects.filter(id=destination_id).first()
            if destination_review is None:
                return Response(errors.REVIEW_NOT_FOUND.get("data"), errors.REVIEW_NOT_FOUND.get("status"))
            like_review = experience_models.LikeReview.objects.filter(destination_review=destination_review,
                                                                      owner=request.user).first()
            if like_review is None:
                destination_review.number_of_likes += 1
                new_like_review = experience_models.LikeReview(owner=request.user,
                                                               destination_review=destination_review)
                new_like_review.save()

            else:
                destination_review.number_of_likes -= 1
                like_review.delete()

            destination_review.save()

        elif destination_type == "COMMENT":
            destination_comment = experience_models.Comment.objects.filter(id=destination_id).first()
            if destination_comment is None:
                return Response(errors.COMMENT_NOT_FOUND.get("data"), errors.COMMENT_NOT_FOUND.get("status"))

            like_comment = experience_models.LikeComment.objects.filter(destination_comment=destination_comment,
                                                                        owner=request.user)
            if like_comment is None:
                new_like_comment = experience_models.LikeComment(owner=request.user,
                                                                 destination_comment=destination_comment)
                new_like_comment.save()
                destination_comment.number_of_likes += 1
            else:
                like_comment.delete()
                destination_comment.number_of_likes -= 1

            destination_comment.save()

        return Response({}, status.HTTP_200_OK)


class Comments(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            destination_post_id = request.data["postId"]
            message = request.data["message"]
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))

        destination_post = experience_models.Post.objects.filter(id=destination_post_id).first()
        if destination_post is None:
            return Response(errors.POST_NOT_FOUND.get("data"), errors.POST_NOT_FOUND.get("status"))

        new_comment = experience_models.Comment(message=message, destination_post=destination_post,
                                                owner=request.user)
        new_comment.save()
        destination_post.save()

        return Response({}, status.HTTP_200_OK)


class ViewAPost(APIView):
    def get(self, request, post_id):
        post = experience_models.Post.objects.filter(id=post_id).first()
        if post is None:
            return Response(errors.POST_NOT_FOUND.get("data"), errors.POST_NOT_FOUND.get("status"))

        like_post = experience_models.LikePost.objects.filter(destination_post=post, owner=request.user)
        return Response(serializers.post_serializer(post, like_post is not None), status.HTTP_200_OK)


class ViewFirstSixPosts(APIView):
    def get(self, request, user_id):
        destination_user = user_models.User.objects.filter(id=user_id).first()
        if destination_user is None:
            if user_id == '-1':
                destination_user = request.user
            else:
                return Response(user_errors.USER_NOT_FOUND.get("data"), user_errors.USER_NOT_FOUND.get("status"))

        all_posts = destination_user.posts.all().order_by('-id')
        posts_count = min(6, len(all_posts))
        first_posts = []
        for index in range(0, posts_count):
            first_posts.append(all_posts[index])

        data = {
            'posts': []
        }
        for index in range(0, posts_count):
            like_post = experience_models.LikePost.objects.filter(destination_post=first_posts[index],
                                                                  owner=request.user).first()
            data['posts'].append(serializers.post_serializer(first_posts[index], like_post is not None))

        return Response(data, status.HTTP_200_OK)


class ViewAllPosts(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        user = user_models.User.objects.filter(id=user_id).first()
        if user is None:
            return Response(user_errors.USER_NOT_FOUND.get("data"), user_errors.USER_NOT_FOUND.get("status"))

        all_posts = user.posts.all().order_by('-id')
        data = {
            "posts": []
        }
        for index in range(0, len(all_posts)):
            like_post = experience_models.LikePost.objects.filter(destination_post=all_posts[index],
                                                                  owner=request.user).first()
            data['posts'].append(serializers.post_serializer(all_posts[index], like_post is not None))

        return Response(data, status.HTTP_200_OK)


class ViewExplorePosts(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        followings = request.user.followings
        pre_index = 0
        first_posts = []
        for destination_user in followings:
            all_posts = destination_user.posts.all()
            posts_count = min(6, len(all_posts))
            for index in range(0, posts_count):
                first_posts.append(all_posts[index])

        first_posts.sort(key=lambda post: post.id, reverse=True)

        data = {
            "posts": []
        }
        for index in range(0, len(first_posts)):
            like_post = experience_models.LikePost.objects.filter(destination_post=first_posts[index],
                                                                  owner=request.user).first()
            data["posts"].append(serializers.post_serializer(first_posts[index - pre_index], like_post is not None))


class ViewFirstReview(APIView):
    def get(self, request, attraction_id):
        attraction = experience_models.Attraction.objects.filter(id=attraction_id)
        if attraction is None:
            return Response(errors.ATTRACTION_NOT_FOUND.get("data"), errors.ATTRACTION_NOT_FOUND.get("status"))
        review = experience_models.Review.objects.filter(attraction=attraction).first()
        if review is None:
            return Response({}, status.HTTP_200_OK)

        like_review = experience_models.LikeReview.objects.filter(destination_review=review, owner=request.user).first()
        return Response(serializers.review_serializer(review, like_review is not None), status.HTTP_200_OK)


class ViewAllReviews(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, attraction_id):
        attraction = experience_models.Attraction.objects.filter(id=attraction_id).first()
        if attraction is None:
            return Response(errors.ATTRACTION_NOT_FOUND.get("data"), errors.ATTRACTION_NOT_FOUND.get("status"))

        all_reviews = attraction.reviews.all()
        data = {
            "reviews": []
        }
        for index in range(0, len(all_reviews)):
            like_review = experience_models.LikeReview.objects.filter(
                destination_review=all_reviews[index], owner=request.user).first()
            data["reviews"].append(serializers.review_serializer(all_reviews[index], like_review is not None))

        return Response(data, status.HTTP_200_OK)


class MyReviews(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_reviews = request.user.reviews.all().order_by('-id')
        data = {
            "reviews": []
        }
        for index in range(0, len(all_reviews)):
            like_review = experience_models.LikeReview.objects.filter(
                destination_review=all_reviews[index], owner=request.user).first()
            data["reviews"].append(serializers.review_serializer(all_reviews[index], like_review is not None))

        return Response(data, status.HTTP_200_OK)


class ViewAllComments(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id):
        post = experience_models.Post.objects.filter(id=post_id).first()
        if post is None:
            return Response(errors.POST_NOT_FOUND.get("data"), errors.POST_NOT_FOUND.get("status"))

        all_comments = post.comments.all().order_by('-number_of_likes')
        data = {
            "comments": []
        }
        for index in range(0, len(all_comments)):
            like_comment = experience_models.LikeComment.objects.filter(destination_comment=all_comments[index],
                                                                        owner=request.user).first()
            data["comments"].append(serializers.comment_serializer(all_comments[index], like_comment is not None))

        return Response(data, status.HTTP_200_OK)


class CityFallowing(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            to_be_subscribed = user_models.City.objects.get(id=request.data["cityId"])
        except user_models.City.DoesNotExist:
            return Response(user_errors.NOT_FOUND.get("data"), user_errors.NOT_FOUND.get("status"))
        except:
            return Response(user_errors.INVALID_ARGUMENTS.get("data"), user_errors.INVALID_ARGUMENTS.get("status"))
        if to_be_subscribed is None:
            return Response(errors.CITY_NOT_FOUND.get("data"), errors.CITY_NOT_FOUND.get("status"))
        else:
            new_following = experience_models.CityFollowings(follower=request.user, following=to_be_subscribed)
            new_following.save()
            return Response({}, status.HTTP_200_OK)
