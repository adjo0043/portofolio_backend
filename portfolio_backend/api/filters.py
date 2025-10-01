"""
Custom filters for API endpoints
"""
from django_filters import rest_framework as filters
from .models import Project, BlogPost, ContactSubmission


class ProjectFilter(filters.FilterSet):
    """
    Filter class for Project model
    """
    title = filters.CharFilter(lookup_expr='icontains')
    technologies = filters.CharFilter(field_name='technologies_used', lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=Project.STATUS_CHOICES)
    is_featured = filters.BooleanFilter()
    tags = filters.CharFilter(field_name='tags__slug', lookup_expr='iexact')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Project
        fields = ['title', 'technologies', 'status', 'is_featured', 'tags']


class BlogPostFilter(filters.FilterSet):
    """
    Filter class for BlogPost model
    """
    title = filters.CharFilter(lookup_expr='icontains')
    content = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter(field_name='author__username', lookup_expr='iexact')
    category = filters.CharFilter(field_name='category__slug', lookup_expr='iexact')
    tags = filters.CharFilter(field_name='tags__slug', lookup_expr='iexact')
    status = filters.ChoiceFilter(choices=BlogPost.STATUS_CHOICES)
    is_featured = filters.BooleanFilter()
    published_after = filters.DateTimeFilter(field_name='published_date', lookup_expr='gte')
    published_before = filters.DateTimeFilter(field_name='published_date', lookup_expr='lte')
    search = filters.CharFilter(method='filter_search')
    
    class Meta:
        model = BlogPost
        fields = ['title', 'author', 'category', 'tags', 'status', 'is_featured']
    
    def filter_search(self, queryset, name, value):
        """
        Custom search filter for title, excerpt, and content
        """
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(excerpt__icontains=value) |
            models.Q(content__icontains=value)
        )


class ContactSubmissionFilter(filters.FilterSet):
    """
    Filter class for ContactSubmission model
    """
    name = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=ContactSubmission.STATUS_CHOICES)
    submitted_after = filters.DateTimeFilter(field_name='submitted_at', lookup_expr='gte')
    submitted_before = filters.DateTimeFilter(field_name='submitted_at', lookup_expr='lte')
    
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'status']


# Import models for Q object
from django.db import models
