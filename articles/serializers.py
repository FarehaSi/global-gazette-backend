from rest_framework import serializers
from .models import Article, Comment, Reaction, Category, Tag

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'like_count', 'dislike_count', 'comment_count']
    
    def get_like_count(self, obj):
        return obj.article_reactions.filter(reaction_type='like').count()

    def get_dislike_count(self, obj):
        return obj.article_reactions.filter(reaction_type='dislike').count()

    def get_comment_count(self, obj):
        return obj.comments.count()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id', 'user', 'article', 'comment', 'reaction_type', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField() 
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'article', 'parent', 'text', 'created_at', 'updated_at', 'replies', 'like_count', 'dislike_count']
        read_only_fields = ['user']

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all(), many=True).data

    def get_like_count(self, obj):
        return obj.comment_reactions.filter(reaction_type='like').count()

    def get_dislike_count(self, obj):
        return obj.comment_reactions.filter(reaction_type='dislike').count()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']