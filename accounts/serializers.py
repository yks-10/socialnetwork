from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Friendship

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class FriendshipSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
