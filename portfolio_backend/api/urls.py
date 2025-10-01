from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    BlogPostViewSet,
    ContactSubmissionViewSet,
    CategoryViewSet,
    TagViewSet,
    SubscriberViewSet,
    HealthCheckViewSet
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'blog', BlogPostViewSet, basename='blogpost')
router.register(r'contact', ContactSubmissionViewSet, basename='contact')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'subscribe', SubscriberViewSet, basename='subscriber')
router.register(r'health', HealthCheckViewSet, basename='health')

urlpatterns = [
    path('', include(router.urls)),
]