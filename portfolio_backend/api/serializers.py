from rest_framework import serializers
from .models import Project, BlogPost, ContactSubmission, Category, Tag, Subscriber
from django.contrib.auth.models import User
import re


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model"""
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count']
        read_only_fields = ['id', 'slug']
    
    def get_post_count(self, obj):
        return obj.blog_posts.filter(status='published').count()


class ProjectListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for project listings"""
    tags = TagSerializer(many=True, read_only=True)
    technology_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'slug',
            'short_description',
            'thumbnail',
            'technology_list',
            'tags',
            'project_url',
            'github_url',
            'is_featured',
            'views_count',
            'created_at'
        ]
        read_only_fields = ['id', 'slug', 'views_count', 'created_at']
    
    def get_technology_list(self, obj):
        """Convert comma-separated string to list"""
        return [tech.strip() for tech in obj.technologies_used.split(',') if tech.strip()]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single project view"""
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Tag.objects.all(),
        source='tags',
        required=False
    )
    technology_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'short_description',
            'image',
            'thumbnail',
            'technologies_used',
            'technology_list',
            'tags',
            'tag_ids',
            'project_url',
            'github_url',
            'demo_url',
            'meta_title',
            'meta_description',
            'status',
            'is_featured',
            'views_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'thumbnail', 'views_count', 'created_at', 'updated_at']
    
    def get_technology_list(self, obj):
        """Convert comma-separated string to list"""
        return [tech.strip() for tech in obj.technologies_used.split(',') if tech.strip()]
    
    def validate_technologies_used(self, value):
        """Ensure technologies are properly formatted"""
        techs = [tech.strip() for tech in value.split(',') if tech.strip()]
        if not techs:
            raise serializers.ValidationError("At least one technology must be specified")
        return ', '.join(techs)


class BlogPostListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for blog post listings"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_email = serializers.EmailField(source='author.email', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'featured_image',
            'author_name',
            'author_email',
            'category_name',
            'tags',
            'is_featured',
            'views_count',
            'reading_time',
            'published_date'
        ]
        read_only_fields = ['id', 'slug', 'views_count', 'reading_time', 'published_date']


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single blog post view"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_email = serializers.EmailField(source='author.email', read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Category.objects.all(),
        source='category',
        required=False,
        allow_null=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Tag.objects.all(),
        source='tags',
        required=False
    )
    
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'content',
            'featured_image',
            'author',
            'author_name',
            'author_email',
            'category_detail',
            'category_id',
            'tags',
            'tag_ids',
            'meta_title',
            'meta_description',
            'status',
            'is_featured',
            'views_count',
            'reading_time',
            'published_date',
            'updated_at'
        ]
        read_only_fields = [
            'id', 'slug', 'author', 'views_count', 
            'reading_time', 'published_date', 'updated_at'
        ]
    
    def validate_content(self, value):
        """Ensure content is substantial"""
        if len(value.strip()) < 100:
            raise serializers.ValidationError(
                "Blog post content must be at least 100 characters"
            )
        return value


class ContactSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for ContactSubmission model with validation"""
    
    class Meta:
        model = ContactSubmission
        fields = [
            'id',
            'name',
            'email',
            'subject',
            'message',
            'phone',
            'submitted_at'
        ]
        read_only_fields = ['id', 'submitted_at']

    def validate_email(self, value):
        """Validate email format"""
        if not value:
            raise serializers.ValidationError("Email is required")
        
        # Basic email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email format")
        
        return value.lower()

    def validate_name(self, value):
        """Validate name"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters")
        
        # Check for suspicious patterns
        if re.search(r'https?://|www\.', value, re.IGNORECASE):
            raise serializers.ValidationError("Name cannot contain URLs")
        
        return value.strip()

    def validate_message(self, value):
        """Ensure message is not empty and not spam"""
        message = value.strip()
        
        if len(message) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters")
        
        if len(message) > 5000:
            raise serializers.ValidationError("Message cannot exceed 5000 characters")
        
        # Check for excessive links (potential spam)
        link_count = len(re.findall(r'https?://', message, re.IGNORECASE))
        if link_count > 3:
            raise serializers.ValidationError("Message contains too many links")
        
        return message

    def validate_phone(self, value):
        """Validate phone number if provided"""
        if not value:
            return value
        
        # Remove common formatting characters
        cleaned = re.sub(r'[\s\-\(\)\+]', '', value)
        
        # Check if it's a valid phone format
        if not re.match(r'^\d{10,15}$', cleaned):
            raise serializers.ValidationError("Invalid phone number format")
        
        return value


class SubscriberSerializer(serializers.ModelSerializer):
    """Serializer for newsletter subscribers"""
    
    class Meta:
        model = Subscriber
        fields = ['id', 'email', 'is_active', 'subscribed_at']
        read_only_fields = ['id', 'is_active', 'subscribed_at']
    
    def validate_email(self, value):
        """Validate email and check for existing subscription"""
        if not value:
            raise serializers.ValidationError("Email is required")
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email format")
        
        # Check if already subscribed
        if Subscriber.objects.filter(email=value.lower(), is_active=True).exists():
            raise serializers.ValidationError("This email is already subscribed")
        
        return value.lower()