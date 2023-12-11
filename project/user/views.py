import random

from django.shortcuts import render
from . import models
from . import errors
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
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))

        if models.User.objects.filter(username=username).first() is not None:
            return Response(errors.DUPLICATE_USERNAME.get("data"), errors.DUPLICATE_USERNAME.get("status"))
        request.user.username = username
        request.user.password = password
        request.user.phone = phone
        request.user.save()

        return Response({}, status.HTTP_200_OK)


class Token(APIView):
    def post(self, request):
        try:
            data = {
                "username": request.data["username"],
                "password": request.data["password"]
            }
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))

        se = AuthTokenSerializer(data=data, context={"request": request})
        if se.is_valid():
            user = se.validated_data["user"]
            token, created = RestToken.objects.get_or_create(user=user)
            return Response({"token": token.key}, status.HTTP_200_OK)
        else:
            return Response({}, status.HTTP_401_UNAUTHORIZED)


class Following(APIView):
    Serializer = serializers.Follower
    Model = models.Followers
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            to_be_followed = models.User.objects.get(id=request.data["user_id"])
        except models.User.DoesNotExist:
            return Response(errors.USER_NOT_FOUND.get("data"), errors.USER_NOT_FOUND.get("status"))
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))

        if to_be_followed is None:
            return Response(errors.USER_NOT_FOUND.get("data"), errors.USER_NOT_FOUND.get("status"))
        else:
            new_following = models.Followers(follower=request.user, following=to_be_followed)
            new_following.save()
            return Response({}, status.HTTP_200_OK)

    def get(self, request):
        all_fallowing = models.Followers.objects.filter(follower=request.user).all()
        serialized = self.Serializer(all_fallowing, many=True)
        return Response(serialized.data, status.HTTP_200_OK)

    def delete(self, request):
        to_be_unfollowed = models.User.objects.filter(id=request.data("user_id"))

        if to_be_unfollowed is None:
            return Response(errors.USER_NOT_FOUND.get("data"), errors.USER_NOT_FOUND.get("status"))
        else:
            to_be_unfollowed.delete()
            return Response({}, status.HTTP_200_OK)


class Followers(APIView):
    Serializer = serializers.Follower
    Model = models.Followers
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_fallowing = models.Followers.objects.filter(fallowing=request.user).all()
        serialized = self.Serializer(all_fallowing, many=True)
        return Response(serialized.data, status.HTTP_200_OK)


class otp(APIView):
    def post(self, request):
        try:
            email = request.data["email"]
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))

        try:
            username = request.data["username"]
        except:
            username = "user" + str(models.User.objects.latest('id').id + 1)

        duplicate_email = models.User.objects.filter(email=email).first()
        if models.User.objects.filter(username=username).first() is not None:
            return Response(errors.DUPLICATE_USERNAME.get("data"), errors.DUPLICATE_USERNAME.get("status"))
        if models.User.objects.filter(email=email).first() is not None:
            return Response(errors.DUPLICATE_EMAIL.get("data"), errors.DUPLICATE_EMAIL.get("status"))

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
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))
        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return Response(errors.USER_NOT_FOUND.get("data"), errors.USER_NOT_FOUND.get("status"))

        if (timezone.now() - user.otp.created_at).total_seconds() < 120:
            return Response(errors.OTP_WAIT.get("data"), errors.OTP_WAIT.get("status"))
        otp_passkey = generate_otp()
        user.otp.passkey = otp_passkey
        user.otp.save()
        send_otp_email(email, otp_passkey)

        return Response({}, status.HTTP_200_OK)


class Otpvalidaitor(APIView):

    def post(self, request):
        try:
            email = request.data["email"]
            otp_key = request.data["otp"]
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))

        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return Response(errors.USER_NOT_FOUND.get("data"), errors.USER_NOT_FOUND.get("status"))
        if user.otp.passkey is None:
            return Response(errors.OTP_NOT_VALID.get("data"), errors.OTP_NOT_VALID.get("status"))
        if user.otp.passkey != otp_key:
            return Response(errors.OTP_NOT_VALID.get("data"), errors.OTP_NOT_VALID.get("status"))
        if (timezone.now() - user.otp.created_at).total_seconds() > 3600:
            return Response(errors.OTP_EXPIRED.get("data"), errors.OTP_EXPIRED.get("status"))

        user.otp.passkey = None
        user.otp.save()

        token, created = RestToken.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
