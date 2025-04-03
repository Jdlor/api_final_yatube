from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView
)

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet


router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('groups', GroupViewSet, basename='group')
router.register('follow', FollowViewSet, basename='followers')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('v1/jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('v1/jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('v1/jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
]
