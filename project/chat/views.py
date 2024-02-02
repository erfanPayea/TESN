from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user import models as user_models

from . import errors
from . import models
from . import serializers


class Message(APIView):
    Serializer = serializers.MessageSerializer
    Model = models.Message
    permission_classes = (IsAuthenticated,)

    def post(self, request, chat_id):
        try:
            content = request.data["content"]
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))
        try:
            chat = models.Chat.objects.get(id=chat_id)
        except models.Chat.DoesNotExist:
            return Response(errors.CHAT_NOT_FOUND.get("data"), errors.CHAT_NOT_FOUND.get("status"))

        new_message = models.Message(chat=chat, sender=request.user, content=content)
        new_message.save()
        serialized = self.Serializer(new_message)
        return Response(serialized.data, status.HTTP_200_OK)

    def get(self, request, chat_id):
        try:
            chat = models.Chat.objects.get(id=chat_id)
        except models.Chat.DoesNotExist:
            return Response(errors.CHAT_NOT_FOUND.get("data"), errors.CHAT_NOT_FOUND.get("status"))
        serialized = self.Serializer(chat.messages, many=True)
        return Response(serialized.data, status.HTTP_200_OK)


    def delete(self, request, chat_id):
        try:
            messageId = request.data["messageId"]
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))
        try:
            chat = models.Chat.objects.get(id=chat_id)
            message = models.Message.objects.get(id=messageId)
        except models.Chat.DoesNotExist:
            return Response(errors.CHAT_NOT_FOUND.get("data"), errors.CHAT_NOT_FOUND.get("status"))
        except models.Message.DoesNotExist:
            return Response(errors.MESSAGE_NOT_FOUND.get("data"), errors.MESSAGE_NOT_FOUND.get("status"))
        message.delete()
        return Response({}, status.HTTP_200_OK)


class Chat(APIView):
    Serializer = serializers.ChatSerializer
    Model = models.Chat
    permission_classes = (IsAuthenticated,)

    def post(self, request, chat_id=0):
        try:
            userId = request.data["userId"]
        except:
            return Response(errors.INVALID_ARGUMENTS.get("data"), errors.INVALID_ARGUMENTS.get("status"))
        if userId == request.user.id:
            return Response(errors.CHAT_WITH_SELF.get("data"), errors.CHAT_WITH_SELF.get("status"))
        try:
            user = user_models.User.objects.get(id=userId)
        except user_models.User.DoesNotExist:
            return Response(errors.USER_NOT_FOUND.get("data"), errors.USER_NOT_FOUND.get("status"))

        existing_chat = models.Chat.objects.filter(
            Q(first_user=user, second_user=request.user) | Q(second_user=user, first_user=request.user)).all()
        if len(existing_chat):
            return Response(errors.ALREADY_EXISTS.get("data"), errors.ALREADY_EXISTS.get("status"))
        new_chat = models.Chat(first_user=request.user, second_user=user)
        new_chat.save()
        serialized = self.Serializer(new_chat, context={'request': request})
        return Response(serialized.data, status.HTTP_200_OK)

    def get(self, request, chat_id=0):
        try:
            chat = models.Chat.objects.get(id=chat_id)
        except models.Chat.DoesNotExist:
            return Response(errors.CHAT_NOT_FOUND.get("data"), errors.CHAT_NOT_FOUND.get("status"))

        serialized = self.Serializer(chat, context={'request': request})
        return Response(serialized.data, status.HTTP_200_OK)


class AllChats(APIView):
    Serializer = serializers.ChatSerializer
    Model = models.Chat
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        chats = models.Chat.objects.filter(Q(second_user=request.user) | Q(first_user=request.user)).all()
        serialized = self.Serializer(chats, many=True, context={'request': request})
        return Response(serialized.data, status.HTTP_200_OK)
