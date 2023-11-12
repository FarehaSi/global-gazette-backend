from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Article, Comment, Reaction, Category, Tag
from django.shortcuts import get_object_or_404
from cloudinary.models import CloudinaryField

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
    truncated_content = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    
    thumbnail = CloudinaryField('image', folder='article_thumbnails/', null=True, blank=True)

    class Meta:
        model = Article
        fields = [
            'id', 'author', 'title', 'truncated_content', 'content', 'thumbnail',
            'category', 'tags', 'created_at', 'updated_at',
            'like_count', 'dislike_count', 'comment_count'
        ]
        extra_kwargs = {
            'content': {'write_only': True},
            'truncated_content': {'read_only': True},
        }
    def get_truncated_content(self, obj):
        return (obj.content[:100] + '...') if len(obj.content) > 100 else obj.content


    def get_like_count(self, obj):
        return obj.article_reactions.filter(reaction_type='like').count()

    def get_dislike_count(self, obj):
        return obj.article_reactions.filter(reaction_type='dislike').count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        category_data = validated_data.pop('category', None)

        article = Article.objects.create(**validated_data)

        if category_data:
            article.category = category_data

        if tags_data:
            for tag_data in tags_data:
                article.tags.add(tag_data)

        article.save()
        return article
    

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'request' in self.context and self.context['request'].parser_context['kwargs'].get('pk'):
            ret['content'] = instance.content
        return ret