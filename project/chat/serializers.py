from rest_framework.serializers import ModelSerializer
from . import models
from user import models as user_models


class UserSerializer(ModelSerializer):
    class Meta:
        model = user_models.User
        fields = (
            "username",
            "id",
        )


class MessageSerializer(ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = models.Message
        fields = (
            "sender",
            "date",
            "content"
        )


class ChatSerializer(ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Chat
        fields = '__all__'