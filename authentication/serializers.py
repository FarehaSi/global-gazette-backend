from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'full_name', 'followers_count')
        extra_kwargs = {'password': {'write_only': True}}

    def get_followers_count(self, obj):
        return obj.followers.count()
