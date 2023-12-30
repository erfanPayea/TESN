from django.shortcuts import render
from . import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class Message(APIView):
    Serializer = serializers.Message
    Model = models.Message
    permission_classes = (IsAuthenticated,)

    def get(self, request, chat_id):
        messages_in_chat = models.Chat.objects.filter(id=chat_id).messages.all()
        if messages_in_chat is None:
            return Response({}, status.HTTP_400_BAD_REQUEST)

        serialized = self.Serializer(messages_in_chat, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status.HTTP_200_OK)
        else:
            return Response({}, status.HTTP_400_BAD_REQUEST)

    def post(self, request, chat_id):

        try:
            content = request.data["content"]
        except:
            return Response({}, status.HTTP_400_BAD_REQUEST)
        chat = models.Chat.objects.filter(id=chat_id).first()
        if chat is None:
            return Response({}, status.HTTP_400_BAD_REQUEST)

        new_message = models.Message(chat=chat, sender=request.user, content=request.content)
        new_message.save()  # todo: A message from Erfan: Is not better to save after validation ?

        serialized = self.Serializer(new_message)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status.HTTP_200_OK)
        else:
            return Response({}, status.HTTP_400_BAD_REQUEST)
