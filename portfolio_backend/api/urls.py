from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, BlogPostViewSet, ContactSubmissionViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'blog', BlogPostViewSet, basename='blogpost')
router.register(r'contact', ContactSubmissionViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
]