from django.shortcuts import render

# Create your views here.
from . import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token as RestToken


class Users(APIView):
    permission_classes =()

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
        se.is_valid(raise_exception=True)
        user = se.validated_data["user"]
        token, created = RestToken.objects.get_or_create(user=user)

        return Response({"token": token.key}, status.HTTP_200_OK)