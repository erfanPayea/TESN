from rest_framework.serializers import ModelSerializer
from . import models


class MessageSerializer(ModelSerializer):
    class Meta:
        models = models.Chat
        fields = (
            "sender",
            "date",
            "content"
        )


class ChatSerializer(ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        models = models.Chat
        fields = (
            "second_user",
            "first_user",
            "created_at",
            "messages",
        )
