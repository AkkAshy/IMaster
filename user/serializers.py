from rest_framework import serializers
from .models import User, SupportMessage, UserAction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'email', 'profile_picture', 'role']


class SupportMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMessage
        fields = ['id', 'sender', 'subject', 'message', 'sent_at', 'is_resolved']
        read_only_fields = ['id', 'sender', 'sent_at', 'is_resolved']


class UserActionSerializer(serializers.ModelSerializer):
    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserAction
        fields = ['id', 'user', 'action_type', 'action_type_display', 'description', 'created_at']
        read_only_fields = ['user', 'created_at', 'action_type_display']