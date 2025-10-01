from rest_framework import serializers
from .models import Project, BlogPost, ContactSubmission
from django.contrib.auth.models import User


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model"""
    
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'image',
            'technologies_used',
            'project_url',
            'github_url',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost model"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'author',
            'author_name',
            'published_date',
            'updated_at'
        ]
        read_only_fields = ['id', 'author', 'published_date', 'updated_at']


class ContactSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for ContactSubmission model"""
    
    class Meta:
        model = ContactSubmission
        fields = [
            'id',
            'name',
            'email',
            'message',
            'submitted_at'
        ]
        read_only_fields = ['id', 'submitted_at']

    def validate_email(self, value):
        """Validate email format"""
        if not value:
            raise serializers.ValidationError("Email is required")
        return value.lower()

    def validate_message(self, value):
        """Ensure message is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        return value