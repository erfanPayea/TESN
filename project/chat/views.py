from django.shortcuts import render
from . import models
from user import models as user_models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from rest_framework.permissions import IsAuthenticated
from . import errors
from django.db.models import Q


# Create your views here.


class Message(APIView):
    Serializer = serializers.MessageSerializer
    Model = models.Message
    permission_classes = (IsAuthenticated,)

    def post(self, request, chat_id):

        try:
            content = request.data["content"]
        except:
            return Response({}, status.HTTP_400_BAD_REQUEST)
        chat = models.Chat.objects.filter(id=chat_id).first()
        if chat is None:
            return Response({}, status.HTTP_400_BAD_REQUEST)

        new_message = models.Message(chat=chat, sender=request.user, content=request.content)

        serialized = self.Serializer(new_message)
        if serialized.is_valid():
            new_message.save()
            serialized.save()
            return Response(serialized.data, status.HTTP_200_OK)
        else:
            return Response({serialized.errors}, status.HTTP_400_BAD_REQUEST)


class Chat(APIView):
    Serializer = serializers.ChatSerializer
    Model = models.Message
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            userId = request.data["userId"]
        except:
            return Response({errors.NECESSARY_FIELDS_REQUIRED}, status.HTTP_400_BAD_REQUEST)
        user = user_models.User.objects.get(id=userId)
        if user is None:
            return Response({errors.USER_NOT_FOUND}, status.HTTP_404_NOT_FOUND)
        existing_chat = models.Chat.objects.filter(Q(first_user=user) | Q(second_user=user)).all()
        if existing_chat is not None:
            return Response({errors.ALREADY_EXISTS}, status.HTTP_400_BAD_REQUEST)
        new_chat = models.Chat(first_user=request.user, second_user=user)
        new_chat.save()
        serialized = self.Serializer(new_chat)
        if serialized.is_valid():
            serialized.save()
            return Response({serialized.data}, status.HTTP_200_OK)
        else:
            return Response(serialized.errors, status.HTTP_400_BAD_REQUEST)

    def get(self, request, chat_id):
        chat = models.Chat.objects.get(id=chat_id)
        if chat is None:
            return Response({errors.CHAT_NOT_FOUND}, status.HTTP_404_NOT_FOUND)

        serialized = self.Serializer(chat)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status.HTTP_200_OK)
        else:
            return Response({serialized.errors}, status.HTTP_400_BAD_REQUEST)
