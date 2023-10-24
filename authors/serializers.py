from rest_framework import serializers
from .models import Author
from authentication.models import CustomUser

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'user', 'followers']
