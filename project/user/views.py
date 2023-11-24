from django.shortcuts import render
from . import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token as RestToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class Users(APIView):
    permission_classes = ()

    def post(self, request):

        username = request.data["username"]
        password = request.data["password"]
        phone = request.data["phone"]

        user = models.User.objects.create_user(username=username, phone=phone, is_staff=True, password=password)
        user.save()

        token, created = RestToken.objects.get_or_create(user=user)

        return Response({"token": token.key}, status.HTTP_200_OK)

        # return Response({}, status.HTTP_204_NO_CONTENT)
        # print("POST")
        # se = serializers.TestApi(data=request.data)
        # if se.is_valid():
        #     se.save()
        #     return Response(se.data, status.HTTP_200_OK)
        # return Response(se.errors, status.HTTP_400_BAD_REQUEST)


class Token(APIView):
    def post(self, request):

        data = {
            "username": request.data["username"],
            "password": request.data["password"]
        }

        se = AuthTokenSerializer(data=data, context={"request": request})
        if se.is_valid():
            user = se.validated_data["user"]
            token, created = RestToken.objects.get_or_create(user=user)
            return Response({"token": token.key}, status.HTTP_200_OK)
        else:
            return Response({}, status.HTTP_401_UNAUTHORIZED)


class Following(APIView):
    Serializer = serializers.Fallowing
    Model = models.Followers
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        to_be_followed = models.User.objects.filter(id=request.data("user_id"))

        if to_be_followed is None:
            return Response({}, status.HTTP_404_NOT_FOUND)
        else:
            new_following = models.Followers(follower=request.user, following=to_be_followed)
            new_following.save()
            return Response({}, status.HTTP_200_OK)

    def get(self, request):
        all_fallowing = models.Followers.objects.filter(fallower=request.user).all()
        serialized = self.Serializer(all_fallowing, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status.HTTP_200_OK)
        else:
            return Response({}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        to_be_unfollowed = models.User.objects.filter(id=request.data("user_id"))

        if to_be_unfollowed is None:
            return Response({}, status.HTTP_404_NOT_FOUND)
        else:
            to_be_unfollowed.delete()
            return Response({}, status.HTTP_200_OK)


class Followers(APIView):
    Serializer = serializers.Fallowing
    Model = models.Followers
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_fallowing = models.Followers.objects.filter(fallowing=request.user).all()
        serialized = self.Serializer(all_fallowing, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status.HTTP_200_OK)
        else:
            return Response({}, status.HTTP_400_BAD_REQUEST)
