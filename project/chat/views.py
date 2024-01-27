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

        new_message = models.Message(chat=chat, sender=request.user, content=content)
        new_message.save()
        serialized = self.Serializer(new_message)
        return Response(serialized.data, status.HTTP_200_OK)



class Chat(APIView):
    Serializer = serializers.ChatSerializer
    Model = models.Chat
    permission_classes = (IsAuthenticated,)

    def post(self, request, chat_id=0):
        try:
            userId = request.data["userId"]
        except:
            return Response({errors.NECESSARY_FIELDS_REQUIRED}, status.HTTP_400_BAD_REQUEST)
        if userId == request.user.id:
            return Response({"you can not chat with yourself!"}, status.HTTP_400_BAD_REQUEST)
        try: user = user_models.User.objects.get(id=userId)
        except models.Chat.DoesNotExist: return Response({errors.USER_NOT_FOUND}, status.HTTP_404_NOT_FOUND)

        existing_chat = models.Chat.objects.filter(Q(first_user=user, second_user=request.user)| Q(second_user=user, first_user=request.user)).all()
        if len(existing_chat):
            return Response({errors.ALREADY_EXISTS}, status.HTTP_400_BAD_REQUEST)
        new_chat = models.Chat(first_user=request.user, second_user=user)
        new_chat.save()
        serialized = self.Serializer(new_chat)
        return Response(serialized.data, status.HTTP_200_OK)


    def get(self, request, chat_id=0):
        print(chat_id)
        try:chat = models.Chat.objects.get(id=chat_id)
        except models.Chat.DoesNotExist: return Response({errors.CHAT_NOT_FOUND}, status.HTTP_404_NOT_FOUND)

        serialized = self.Serializer(chat)
        return Response(serialized.data, status.HTTP_200_OK)

