from django.shortcuts import render
from . import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from .utils import generate_otp, send_otp_email
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token as RestToken
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta

# Create your views here.


class Users(APIView):
    permission_classes = ()

    def post(self, request):

        username = request.data["username"]
        password = request.data["password"]
        phone = request.data["phone"]
        email = request.data["email"]
        duplicate_user = models.User.objects.filter(username=username).first()

        if not duplicate_user is None:
            return Response({'error':'username already exists'}, status.HTTP_400_BAD_REQUEST)

        user = models.User.objects.create_user(username=username, phone=phone, is_staff=True, password=password)
        user.save()
        models.Opt(user=user, passkey=generate_otp()).save()
        send_otp_email(email, otp)

        # token, created = RestToken.objects.get_or_create(user=user)

        return Response({}, status.HTTP_200_OK)

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

class otp(APIView):
    def post(self, request):
        email = request.data["email"]
        otp_key = email = request.data["otp"]

        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if user.otp.passkey is None:
            return Response({'error': 'invalid otp.'}, status=status.HTTP_400_BAD_REQUEST)
        if user.otp.passkey != otp:
            return Response({'error': 'incorrect OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        if datetime.now() - user.otp.created_at > timedelta(minutes=2):
            return Response({'error': 'passkey has been expired.'}, status=status.HTTP_400_BAD_REQUEST)

        user.otp.passkey = None
        user.save()

        token, created = RestToken.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

    def patch(self, request):
        email = request.data["email"]
        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if datetime.now() - user.otp.created_at <= timedelta(minutes=2):
            return Response({'error': 'wait 2 minutes.'}, status=status.HTTP_400_BAD_REQUEST)
        models.Opt(user=user, passkey=generate_otp()).save()
        send_otp_email(email, otp)
        
        return Response({}, status.HTTP_200_OK)


