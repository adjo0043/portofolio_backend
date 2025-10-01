from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, BlogPost, ContactSubmission
from .serializers import (
    ProjectSerializer,
    BlogPostSerializer,
    ContactSubmissionSerializer
)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing projects.
    Provides list() and retrieve() actions.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing blog posts.
    Provides list() and retrieve() actions.
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'  # Allow lookup by slug instead of pk


class ContactSubmissionViewSet(mixins.CreateModelMixin,
                               viewsets.GenericViewSet):
    """
    ViewSet for creating contact submissions.
    Only provides create() action.
    """
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer

    def create(self, request, *args, **kwargs):
        """Handle contact form submission"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {
                'message': 'Thank you for your message! We will get back to you soon.',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )