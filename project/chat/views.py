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


class Message(APIView):
    Serializer = serializers.Message
    Model = models.Message
    permission_classes = (IsAuthenticated, )

    def get(self, request, chat_id):
        messages_in_chat = models.Chat.objects.filter(id=chat_id).messages.all()
        serialized = self.Serializer(messages_in_chat, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status.HTTP_200_OK)
        else:
            return Response({}, status.HTTP_400_BAD_REQUEST)
