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
            attraction_id = request.data["attraction_id"]
            caption = request.data["caption"]
            file_path = request.data["file_path"]
        except:
            return Response(errors.NECESSARY_FIELDS_REQUIRED, status.HTTP_400_BAD_REQUEST)

        attraction = experience_models.Attraction.objects.filter(id=attraction_id).first()
        if attraction is None and attraction_id != "-1":
            return Response(errors.ATTRACTION_NOT_FOUND, status.HTTP_400_BAD_REQUEST)

        new_post = experience_models.Post(owner=request.user, attraction=attraction, number_of_likes=0, caption=caption,
                                          file_path=file_path)
        new_post.save()
        return Response(serializers.post_serializer(new_post), status.HTTP_200_OK)


class Reviews(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            attraction_id = request.data["attraction_id"]
            caption = request.data["caption"]
            file_path = request.data["file_path"]
        except:
            return Response(errors.NECESSARY_FIELDS_REQUIRED, status.HTTP_400_BAD_REQUEST)

        attraction = experience_models.Attraction.objects.filter(id=attraction_id)
        if attraction is None:
            return Response(errors.ATTRACTION_NOT_FOUND, status.HTTP_404_NOT_FOUND)
        new_review = experience_models.Review(owner=request.user, attraction=attraction, number_of_likes=0,
                                              caption=caption, file_path=file_path)
        new_review.save()
        return Response(serializers.review_serializer(new_review), status.HTTP_200_OK)


class Likes(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            destination_type = request.data["destination_type"]
            destination_id = request.data["destination_id"]
        except:
            return Response(errors.NECESSARY_FIELDS_REQUIRED, status.HTTP_400_BAD_REQUEST)

        if destination_type == "POST":
            destination_post = experience_models.Post.objects.filter(id=destination_id).first()
            if destination_post is None:
                return Response(errors.POST_NOT_FOUND, status.HTTP_400_BAD_REQUEST)
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
                return Response(errors.REVIEW_NOT_FOUND, status.HTTP_404_NOT_FOUND)
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
                return Response(errors.COMMENT_NOT_FOUND, status.HTTP_404_NOT_FOUND)

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


class ViewAPost(APIView):
    def get(self, request, post_id):
        post = experience_models.Post.objects.filter(id=post_id).first()
        if post is None:
            return Response(errors.POST_NOT_FOUND, status.HTTP_404_NOT_FOUND)
        return Response(serializers.post_serializer(post), status.HTTP_200_OK)


class ViewFirstSixPosts(APIView):
    def get(self, request, user_id):
        user = user_models.User.objects.filter(id=user_id).first()
        if user is None:
            return Response(errors.USER_NOT_FOUND, status.HTTP_400_BAD_REQUEST)
        posts_count = min(6, len(user.posts.all()))
        posts = []
        for index in range(0, posts_count):
            posts.append(user.posts.all()[index])

        data = {}
        for index in range(0, posts_count):
            data[f"{index}"] = serializers.post_serializer(posts[index])
        return Response(data, status.HTTP_200_OK)


class ViewAllPosts(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        user = user_models.User.objects.filter(id=user_id).first()
        if user is None:
            return Response(errors.USER_NOT_FOUND, status.HTTP_400_BAD_REQUEST)

        data = {}
        for index in range(0, len(user.posts.all())):
            data[f"{index}"] = serializers.post_serializer(user.posts.all()[index])
        return Response(data, status.HTTP_200_OK)


class ViewFirstReview(APIView):
    def get(self, request, attraction_id):
        attraction = experience_models.Attraction.objects.filter(id=attraction_id)
        if attraction is None:
            return Response(errors.ATTRACTION_NOT_FOUND, status.HTTP_400_BAD_REQUEST)
        review = experience_models.Review.objects.filter(attraction=attraction).first()
        if review is None:
            return Response({}, status.HTTP_200_OK)

        return Response(serializers.review_serializer(review), status.HTTP_200_OK)


class ViewAllReviews(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, attraction_id):
        attraction = experience_models.Attraction.objects.filter(id=attraction_id).first()
        if attraction is None:
            return Response(errors.ATTRACTION_NOT_FOUND, status.HTTP_400_BAD_REQUEST)

        data = {}
        for index in range(0, len(attraction.reviews.all())):
            data[f"{index}"] = serializers.review_serializer(attraction.reviews.all()[index])
        return Response(data, status.HTTP_200_OK)


class ViewBestComment(APIView):
    def get(self, request, post_id):
        post = experience_models.Post.objects.filter(id=post_id).first()
        if post is None:
            return Response(errors.POST_NOT_FOUND, status.HTTP_404_NOT_FOUND)

        maximum = -1
        best_comment_index = -1
        for index in range(0, len(post.comments.all())):
            if post.comments.all()[index].number_of_likes > maximum:
                best_comment_index = index

        if best_comment_index == -1:
            return Response({}, status.HTTP_200_OK)
        return Response(serializers.comment_serializer(post.comments.all()[best_comment_index]), status.HTTP_200_OK)


class ViewAllComments(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id):
        post = experience_models.Post.objects.filter(id=post_id).first()
        if post is None:
            return Response(errors.POST_NOT_FOUND, status.HTTP_404_NOT_FOUND)

        data = {}
        for index in range(0, len(post.comments.all())):
            data[f"{index}"] = serializers.comment_serializer(post.comments.all()[index])
        return Response(data, status.HTTP_200_OK)



class CityFallowing(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            to_be_subscribed = user_models.City.objects.get(id=request.data["city_id"])
        except user_models.User.DoesNotExist:
            return Response(user_errors.NOT_FOUND.get("data"), user_errors.NOT_FOUND.get("status"))
        except:
            return Response(user_errors.INVALID_ARGUMENTS.get("data"), user_errors.INVALID_ARGUMENTS.get("status"))
        if to_be_subscribed is None:
            return Response(user_errors.NOT_FOUND.get("data"), user_errors.USER_NOT_FOUND.get("status"))
        else:
            new_following = experience_models.CityFollowings(follower=request.user, following=to_be_subscribed)
            new_following.save()
            return Response({}, status.HTTP_200_OK)