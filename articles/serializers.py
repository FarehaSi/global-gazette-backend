from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Article, Comment, Reaction, Category, Tag

# class ArticleSerializer(serializers.ModelSerializer):
#     author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
#     like_count = serializers.SerializerMethodField()
#     dislike_count = serializers.SerializerMethodField()
#     comment_count = serializers.SerializerMethodField()
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
#     thumbnail = serializers.ImageField(max_length=None, use_url=True)
#     class Meta:
#         model = Article
#         fields = [
#             'id', 'author', 'title', 'content', 'thumbnail', 'category', 'tags', 
#             'created_at', 'updated_at', 'like_count', 'dislike_count', 'comment_count'
#         ]
    
#     def get_like_count(self, obj):
#         return obj.article_reactions.filter(reaction_type='like').count()

#     def get_dislike_count(self, obj):
#         return obj.article_reactions.filter(reaction_type='dislike').count()

#     def get_comment_count(self, obj):
#         return obj.comments.count()

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

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

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True) 
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    thumbnail = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Article
        fields = [
            'id', 'author', 'title', 'content', 'thumbnail', 'category', 'tags',
            'created_at', 'updated_at', 'like_count', 'dislike_count', 'comment_count'
        ]

    def get_like_count(self, obj):
        return obj.article_reactions.filter(reaction_type='like').count()

    def get_dislike_count(self, obj):
        return obj.article_reactions.filter(reaction_type='dislike').count()

    def get_comment_count(self, obj):
        return obj.comments.count()