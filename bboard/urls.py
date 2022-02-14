from django.urls import path, include
from rest_framework import routers

from bboard import views
from .yasg import urlpatterns as doc_urls


router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='posts')
router.register(r'comment', views.CommentCreateView, basename='comment')
router.register(r'private', views.PrivatePageView, basename='private')

urlpatterns = [
    path('', include(router.urls)),
]
# Include swagger docs
urlpatterns += doc_urls
