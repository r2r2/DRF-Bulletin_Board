from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from bboard.models import Post, Comment
from bboard.permissions import IsOwnerOrReadOnly
from bboard.serializers import (PostListSerializer,
                                PostDetailSerializer,
                                CommentCreateSerializer,
                                CommentSerializer,
                                PostCreateSerializer,
                                PrivatePageSerializer)
from bboard.service import CommentFilter


class PostViewSet(viewsets.ModelViewSet):
    """CRUD for Post model"""
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        elif self.action == 'create':
            return PostCreateSerializer
        else:
            return PostListSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentCreateView(viewsets.ModelViewSet):
    """Write a comment"""
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PrivatePageView(viewsets.ModelViewSet):
    """Private page where User can see only comments to his Posts"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CommentFilter
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user_comments = Comment.objects.filter(post__owner=self.request.user)
        return user_comments

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentSerializer
        elif self.action == 'update' or 'destroy' or 'retrieve' or 'partial_update':
            return PrivatePageSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
