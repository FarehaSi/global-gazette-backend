from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Author
from .serializers import AuthorSerializer

class FollowAuthorView(APIView):
    def post(self, request, author_id):
        try:
            author_to_follow = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response({'detail': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.author == author_to_follow:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.author.followers.add(author_to_follow)
        return Response({'detail': f'You are now following {author_to_follow.user.username}.'})

    def delete(self, request, author_id):
        try:
            author_to_unfollow = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response({'detail': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

        request.user.author.followers.remove(author_to_unfollow)
        return Response({'detail': f'You have unfollowed {author_to_unfollow.user.username}.'})
