from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers as django_serializers

from user import models as user_models
from . import models as experience_models
from . import serializers


class Posts(APIView):
    permission_classes = (IsAuthenticated,)
    Serializer = serializers.Post

    def post(self, request):
        attraction = experience_models.Attraction.objects.filter(id=request.data["attraction_id"])
        new_post = experience_models.Post(owner=request.user, attraction=attraction, number_of_likes=0,
                                          caption=request.data["caption"], file_path=request.data["file_path"])

        serialized = self.Serializer(new_post)
        if serialized.is_valid():
            new_post.save()
            serialized.save()
            return Response(serialized.data, status.HTTP_200_OK)
        else:
            return Response({}, status.HTTP_400_BAD_REQUEST)


class Reviews(APIView):
    permission_classes = (IsAuthenticated,)
    Serializer = serializers.Review

    def post(self, request):
        attraction = experience_models.Attraction.objects.filter(id=request.data["attraction_id"])
        if attraction is None:
            return Response({}, status.HTTP_400_BAD_REQUEST)
        new_review = experience_models.Review(owner=request.user, attraction=attraction, number_of_likes=0,
                                              caption=request.data["caption"], file_path=request.data["file_path"])

        serialized = self.Serializer(new_review)
        if serialized.is_valid():
            new_review.save()
            serialized.save()
            return Response(serialized.data, status.HTTP_200_OK)
        else:
            return Response({}, status.HTTP_400_BAD_REQUEST)


class Likes(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        destination_type = request.data["destination_type"]
        destination_id = request.data["destination_id"]

        if destination_type == "POST":
            destination_post = experience_models.Post.objects.filter(id=destination_id)
            if destination_post is None:
                return Response({}, status.HTTP_400_BAD_REQUEST)
            like_post = experience_models.LikePost(owner=request.user, destination_post=destination_post)
            like_post.save()

        elif destination_type == "REVIEW":
            destination_review = experience_models.Review.objects.filter(id=destination_id)
            if destination_review is None:
                return Response({}, status.HTTP_400_BAD_REQUEST)
            like_review = experience_models.LikeReview(owner=request.user, destination_review=destination_review)
            like_review.save()

        elif destination_type == "COMMENT":
            destination_comment = experience_models.Comment.objects.filter(id=destination_id)
            if destination_comment is None:
                return Response({}, status.HTTP_400_BAD_REQUEST)
            like_comment = experience_models.LikeComment(owner=request.user, destination_comment=destination_comment)
            like_comment.save()

        return Response({}, status.HTTP_200_OK)


class ViewFirstSixPosts(APIView):
    def get(self, request, user_id):
        user = user_models.User.objects.filter(id=user_id).first()
        if user is None:
            return Response({}, status.HTTP_400_BAD_REQUEST)
        posts_count = min(6, len(user.posts))
        posts = []
        for index in range(0, posts_count):
            posts.append(user.posts[index])

        data = django_serializers.serialize("json", posts)  # todo : check if work
        return Response(data, status.HTTP_200_OK)


class ViewAllPosts(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        user = user_models.User.objects.filter(id=user_id).first()
        if user is None:
            return Response({}, status.HTTP_400_BAD_REQUEST)

        data = django_serializers.serialize("json", user.posts)  # todo : check if work
        return Response(data, status.HTTP_200_OK)


class ViewFirstReview(APIView):
    Serializer = serializers.Review

    def get(self, request, attraction_id):
        attraction = experience_models.Attraction.objects.filter(id=attraction_id)
        if attraction is None:
            return Response({}, status.HTTP_400_BAD_REQUEST)

        return Response(self.Serializer(
            experience_models.Review.objects.filter(attraction=attraction).order_by('sent_time').first()),
                        status.HTTP_200_OK)


class ViewAllReviews(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, attraction_id):
        attraction = experience_models.Attraction.objects.filter(id=attraction_id).first()
        if attraction is None:
            return Response({}, status.HTTP_400_BAD_REQUEST)

        data = django_serializers.serialize("json", attraction.reviews)
        return Response(data, status.HTTP_200_OK)
