import random

from django.shortcuts import render
from . import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from .otp import generate_otp, send_otp_email
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token as RestToken
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.


class Users(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]
            phone = request.data["phone"]
        except:
            return Response({'error': 'provide necessary arguments.'}, status=status.HTTP_404_NOT_FOUND)

        request.user.username = username
        request.user.password = password
        request.user.phone = phone
        request.user.save()
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
        try:
            data = {
                "username": request.data["username"],
                "password": request.data["password"]
            }
        except:
            return Response({'error': 'provide necessary arguments.'}, status=status.HTTP_404_NOT_FOUND)

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
        try:
            email = request.data["email"]
        except:
            return Response({'error': 'provide valid email.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            username = request.data["username"]
        except:
            username = "user" + str(models.User.objects.latest('id').id + 1)

        duplicate_email = models.User.objects.filter(email=email).first()
        if models.User.objects.filter(username=username).first() is not None:
            return Response({'error': 'username already exists'}, status.HTTP_400_BAD_REQUEST)
        if models.User.objects.filter(email=email).first() is not None:
            return Response({'error': 'email already exists'}, status.HTTP_400_BAD_REQUEST)

        user = models.User.objects.create_user(username=username, email=email)
        user.save()
        otp_passkey = generate_otp()
        models.Otp(user=user, passkey=otp_passkey).save()
        send_otp_email(email, otp_passkey)
        return Response({}, status.HTTP_200_OK)


    def patch(self, request):
        try:
            email = request.data["email"]
        except:
            return Response({'error': 'provide necessary arguments.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if (timezone.now() - user.otp.created_at).total_seconds() < 120:
            return Response({'error': 'wait 2 minutes.'}, status=status.HTTP_400_BAD_REQUEST)
        otp_passkey = generate_otp()
        user.otp.passkey = otp_passkey
        user.otp.save()
        send_otp_email(email, otp_passkey)
        
        return Response({}, status.HTTP_200_OK)


class otpValidaitor(APIView):

    def post(self, request):
        try:
            email = request.data["email"]
            otp_key = request.data["otp"]
        except:
            return Response({'error': 'provide necessary arguments.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if user.otp.passkey is None:
            return Response({'error': 'invalid otp.'}, status=status.HTTP_400_BAD_REQUEST)
        if user.otp.passkey != otp_key:
            return Response({'error': 'incorrect OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        if (timezone.now() - user.otp.created_at).total_seconds() > 3600:
            return Response({'error': 'passkey has been expired.'}, status=status.HTTP_400_BAD_REQUEST)

        user.otp.passkey = None
        user.otp.save()

        token, created = RestToken.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
