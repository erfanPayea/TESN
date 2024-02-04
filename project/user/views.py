from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token as RestToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import re

from . import errors
from . import models
from . import serializers
from .otp import generate_otp, send_otp_email


class Users(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.data)
        try:
            username = request.data["username"]
            password = request.data["password"]
            phone = request.data["phone"]
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))

        if models.User.objects.filter(username=username).first() is not None:
            return Response(errors.DUPLICATE_USERNAME.get("data"), errors.DUPLICATE_USERNAME.get("status"))
        if len(password) < 8:
            return Response(errors.INVALID_PASSWORD.get("data"), errors.INVALID_PASSWORD.get("status"))

        request.user.set_password(password)
        request.user.username = username
        request.user.phone = phone
        request.user.save()

        return Response({}, status.HTTP_200_OK)

    def get(self, request):
        return Response(serializers.userSerializer(request.user), status.HTTP_200_OK)

    def patch(self, request):
        try:
            password = request.data["password"]
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))
        if len(password) < 8:
            return Response(errors.INVALID_PASSWORD.get("data"), errors.INVALID_PASSWORD.get("status"))
        print(request.user.username)
        request.user.set_password(password)
        request.user.save()
        return Response({}, status.HTTP_200_OK)


class UserDetails(APIView):
    def get(self, request, user_id):
        try:
            destination_user = models.User.objects.get(id=user_id)
        except:
            return Response(errors.USER_NOT_FOUND.get("data"), errors.USER_NOT_FOUND.get("status"))
        return Response(serializers.userSerializer(destination_user), status.HTTP_200_OK)


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
            return Response({"token": token.key, "id": user.id}, status.HTTP_200_OK)
        else:
            return Response(errors.WRONG_PASSWORD.get("data"), errors.WRONG_PASSWORD.get("status"))


class Following(APIView):
    Serializer = serializers.Follower
    Model = models.Followers
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            to_be_followed = models.User.objects.get(id=request.data["userId"])
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
        serialized = self.Serializer(all_fallowing, many=True, context={'request': request})
        return Response(serialized.data, status.HTTP_200_OK)

    def delete(self, request):
        to_be_unfollowed = models.User.objects.filter(id=request.data("userId"))

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
        all_fallowing = models.Followers.objects.filter(following=request.user).all()
        serialized = self.Serializer(all_fallowing, many=True, context={'request': request})
        return Response(serialized.data, status.HTTP_200_OK)


class Otp(APIView):
    def post(self, request, *args, **kwargs):
        print(request.FILES)
        print(request.POST)
        try:
            email = request.POST["email"]
            avatar_image = request.FILES["avatarImage"]
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))

        try:
            username = request.data["username"]
        except:
            try:
                username = "user" + str(models.User.objects.latest('id').id + 1)
            except:
                username = "user"

        if models.User.objects.filter(username=username).first() is not None:
            return Response(errors.DUPLICATE_USERNAME.get("data"), errors.DUPLICATE_USERNAME.get("status"))
        if models.User.objects.filter(email=email).first() is not None:
            return Response(errors.DUPLICATE_EMAIL.get("data"), errors.DUPLICATE_EMAIL.get("status"))

        user = models.User.objects.create_user(username=username, email=email)
        user.avatar_image = avatar_image
        user.save()
        otp_passkey = generate_otp()
        models.Otp(user=user, passkey=otp_passkey).save()
        send_otp_email(email, otp_passkey)
        print("YES!")
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


class OtpValidator(APIView):

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
        if (timezone.now() - user.otp.created_at).total_seconds() > 3600:
            return Response(errors.OTP_EXPIRED.get("data"), errors.OTP_EXPIRED.get("status"))
        if user.otp.passkey is None:
            return Response(errors.OTP_NOT_VALID.get("data"), errors.OTP_NOT_VALID.get("status"))
        if user.otp.passkey != otp_key:
            return Response(errors.OTP_NOT_VALID.get("data"), errors.OTP_NOT_VALID.get("status"))

        user.otp.passkey = None
        user.otp.save()

        token, created = RestToken.objects.get_or_create(user=user)
        return Response({'token': token.key, 'id': user.id}, status=status.HTTP_200_OK)


class Subscribe(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            membership = request.data["membership"]
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))

        # todo : ino khodet neveshti ! :
        # bank transaction validation needed
        if re.fullmatch("[GBS]", membership):
            request.user.membership = membership
            request.user.save()
        else:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))
