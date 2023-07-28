from rest_framework import serializers
from .models import User
from chatbot.models import Conversation

class UserSerializer(serializers.ModelSerializer):
    conversation = serializers.PrimaryKeyRelatedField(many=True, queryset=Conversation.objects.all())

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            nickname = validated_data['nickname'],
            password = validated_data['password']
        )
        return user