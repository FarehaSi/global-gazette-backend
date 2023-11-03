from rest_framework import generics, status, permissions
from django.shortcuts import get_object_or_404
from .models import Reaction, Article, Comment, Category, Tag
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, UpdateAPIView
from .serializers import CommentSerializer, CategorySerializer, ArticleSerializer, TagSerializer
from rest_framework import filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class ArticleListView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def get_queryset(self):
        queryset = Article.objects.all()
        parser_classes = (MultiPartParser, FormParser, JSONParser)
        limit = self.request.query_params.get('limit')
        if limit and limit.isdigit():
            queryset = queryset[:int(limit)]
        
        return queryset

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create an article.")
        serializer.save(author=self.request.user)



# view single article 
class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionDenied("You don't have permission to edit this article.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You don't have permission to delete this article.")
        instance.delete()


# list all user's created articles
class UserArticlesListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

# update user's owned article
class ArticleUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionDenied("You don't have permission to edit this article.")
        serializer.save()

# delete user's owned article
class ArticleDeleteView(generics.DestroyAPIView):
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You don't have permission to delete this article.")
        instance.delete()

class ReactToArticle(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, article_id, reaction_type):
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return Response({"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

        # Try to get an existing reaction
        reaction, created = Reaction.objects.get_or_create(
            user=request.user,
            article=article,
        )

        # If the reaction already exists and is the same as the new action, delete it.
        if not created and reaction.reaction_type == reaction_type:
            reaction.delete()
            return Response({"detail": f"Reaction '{reaction_type}' removed."}, status=status.HTTP_200_OK)
        
        # If the reaction exists but is different from the new action, update it.
        reaction.reaction_type = reaction_type
        reaction.save()

        return Response({"detail": f"Reaction '{reaction_type}' set."}, status=status.HTTP_200_OK)

class ReactToComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id, reaction_type):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        reaction, created = Reaction.objects.get_or_create(
            user=request.user,
            comment=comment,
        )
        if not created and reaction.reaction_type == reaction_type:
            reaction.delete()
            return Response({"detail": f"Reaction '{reaction_type}' removed."}, status=status.HTTP_200_OK)
        
        reaction.reaction_type = reaction_type
        reaction.save()

        return Response({"detail": f"Reaction '{reaction_type}' set."}, status=status.HTTP_200_OK)


class CommentCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        article = Article.objects.get(pk=self.kwargs['article_id'])
        serializer.save(user=self.request.user, article=article)

class CommentUpdateView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().user == self.request.user:
            serializer.save()
        else:
            return Response({"detail": "Not allowed to edit this comment."}, status=status.HTTP_403_FORBIDDEN)

class CommentDeleteView(DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            return Response({"detail": "Not allowed to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

class ReplyToCommentView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        parent_comment = Comment.objects.get(pk=self.kwargs['comment_id'])
        serializer.save(user=self.request.user, article=parent_comment.article, parent=parent_comment)


class ArticleCommentsListView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        article_id = self.kwargs['article_id']
        return Comment.objects.filter(article__id=article_id)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]



class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

class TagRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

class LikedArticlesView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        liked_reactions = Reaction.objects.filter(user=user, reaction_type='like')
        article_ids = liked_reactions.values_list('article', flat=True)
        return Article.objects.filter(id__in=article_ids)