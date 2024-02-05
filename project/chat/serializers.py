from rest_framework.serializers import ModelSerializer
from . import models
from user import models as user_models


class UserSerializer(ModelSerializer):
    class Meta:
        model = user_models.User
        fields = (
            "id",
            "username",
            "avatar_image",
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
    class Meta:
        model = models.Chat
        fields = (
            "id",
            "created_at",
        )

    def to_representation(self, instance):
        # Exclude the current user from the serialized data
        request = self.context.get('request', None)
        current_user = getattr(request, 'user', None)
        data = super().to_representation(instance)
        if instance.first_user == current_user:
            other_user = instance.second_user
        elif instance.second_user == current_user:
            other_user = instance.first_user
        else:
            return data
        data['cantact'] = {
            'id': other_user.id,
            'username': other_user.username,
            'avatarImage': "http://127.0.0.1:8000/media/" + str(other_user.avatar_image)
        }
        return data
