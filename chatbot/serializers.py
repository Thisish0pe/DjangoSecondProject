from rest_framework import serializers
from .models import Conversation

class CoversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['prompt']