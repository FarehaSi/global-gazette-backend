from django.contrib.auth import get_user_model
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'bio', 'profile_picture', 'full_name')
        extra_kwargs = {'password': {'write_only': True}}
