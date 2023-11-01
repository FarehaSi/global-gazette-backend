from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .serializers import CustomUserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save(update_fields=["password"])

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

class FollowUserView(APIView):
    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user_to_follow:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.followers.add(user_to_follow)
        return Response({'detail': f'You are now following {user_to_follow.username}.'})

    def delete(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        request.user.followers.remove(user_to_unfollow)
        return Response({'detail': f'You have unfollowed {user_to_unfollow.username}.'})
