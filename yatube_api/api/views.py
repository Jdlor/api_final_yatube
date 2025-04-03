from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import (
    permissions,
    viewsets,
    mixins,
    filters,
    response,
    pagination
)
from posts.models import Group, Post, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    GroupSerializer,
    PostSerializer,
    FollowSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        if any(param in request.query_params
               for param in ('limit', 'offset')):
            self.pagination_class = pagination.LimitOffsetPagination
            return super().list(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(
            author=self.request.user,
            post=post
        )


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', 'user__username')

    def get_queryset(self):
        user = self.request.user
        search_query = self.request.query_params.get('search')
        if not user.is_authenticated:
            return Comment.objects.none()
        queryset = user.follower.all()
        if search_query:
            return queryset.filter(
                Q(user__username__icontains=search_query)
                | Q(following__username__icontains=search_query)
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
