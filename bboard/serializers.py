from rest_framework import serializers

from bboard.models import Post, Comment, Category


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'post')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    comment = CommentSerializer(many=True)

    class Meta:
        model = Post
        exclude = ('owner',)


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('owner',)


class PrivatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('accepted',)
