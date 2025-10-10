from rest_framework import serializers
from .models import Post, Comment, Like

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_username', 'post', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'title', 'content', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['author', 'created_at', 'updated_at']

class LikeSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    post_title = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Like
        fields = ['id', 'post', 'post_title', 'user', 'user_username', 'created_at']
        read_only_fields = ['user', 'created_at']