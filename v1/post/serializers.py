from v1.post.models import Post, Likes, Profile
from rest_framework.serializers import ModelSerializer, StringRelatedField
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ImageProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_image']

class ListSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    author = StringRelatedField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'published', 'likes', 'is_liked', 'category','blog_image']

    def get_is_liked(self, obj):
        user = self.context['request'].user
        like = Likes.objects.filter(post=obj, user=user).first()
        return like.is_liked if like else False


class DetailSerializer(ModelSerializer):
	author = StringRelatedField()
	class Meta:
		model = Post
		lookup_field = 'pk'
		fields = ('id', 'author', 'title', 'content', 'published', 'updated_at', 'likes', 'category', 'blog_image')


class CreateSerializer(ModelSerializer):
    author = StringRelatedField(read_only=True)
    class Meta:
        model = Post
        fields = ('title', 'content', 'author', 'published', 'likes', 'category', 'blog_image')


class UpdateSerializer(ModelSerializer):
    author = StringRelatedField(read_only=True)
    class Meta:
        model = Post
        fields = ('title', 'content', 'author', 'published', 'updated_at','likes', 'category', 'blog_image') 
        read_only_fields = ('updated_at',)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['is_liked']


