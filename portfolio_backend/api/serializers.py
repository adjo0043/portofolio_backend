from rest_framework import serializers
from .models import (
    Project, BlogPost, ContactSubmission, Category, Tag, Subscriber,
    Profile, Education, SkillGroup, SkillItem, ProjectBullet,
    SocialLink, Experience, ExperienceBullet, Certification, 
    Language, Interest, CustomSection, CustomSectionItem
)
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


# ===== Portfolio Content Serializers =====

class SocialLinkSerializer(serializers.ModelSerializer):
    """Serializer for social media links"""
    platform = serializers.CharField(source='name', read_only=True)
    icon_class = serializers.SerializerMethodField()
    
    class Meta:
        model = SocialLink
        fields = ['id', 'platform', 'url', 'icon', 'icon_class', 'order']
    
    def get_icon_class(self, obj):
        """Return custom icon class if set, otherwise generate from icon choice"""
        if obj.custom_icon_class:
            return obj.custom_icon_class
        icon_mapping = {
            'github': 'fab fa-github',
            'linkedin': 'fab fa-linkedin',
            'twitter': 'fab fa-twitter',
            'facebook': 'fab fa-facebook',
            'instagram': 'fab fa-instagram',
            'youtube': 'fab fa-youtube',
            'dribbble': 'fab fa-dribbble',
            'behance': 'fab fa-behance',
            'medium': 'fab fa-medium',
            'dev': 'fab fa-dev',
            'stackoverflow': 'fab fa-stack-overflow',
            'codepen': 'fab fa-codepen',
            'discord': 'fab fa-discord',
            'telegram': 'fab fa-telegram',
            'whatsapp': 'fab fa-whatsapp',
            'email': 'fas fa-envelope',
            'website': 'fas fa-globe',
        }
        return icon_mapping.get(obj.icon, 'fas fa-link')


class SkillItemSerializer(serializers.ModelSerializer):
    """Serializer for individual skill items"""
    
    class Meta:
        model = SkillItem
        fields = ['id', 'name', 'proficiency', 'order']


class SkillGroupSerializer(serializers.ModelSerializer):
    """Serializer for skill groups with nested items"""
    items = SkillItemSerializer(many=True, read_only=True)
    name = serializers.CharField(source='title', read_only=True)
    
    class Meta:
        model = SkillGroup
        fields = ['id', 'name', 'icon', 'order', 'items']


class EducationSerializer(serializers.ModelSerializer):
    """Serializer for education entries - maps to frontend Education type"""
    institution = serializers.CharField(source='subtitle', read_only=True)
    degree = serializers.CharField(source='title', read_only=True)
    field_of_study = serializers.CharField(source='title', read_only=True)
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    is_current = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    gpa = serializers.SerializerMethodField()
    institution_logo = serializers.SerializerMethodField()
    
    class Meta:
        model = Education
        fields = [
            'id', 'institution', 'degree', 'field_of_study',
            'start_date', 'end_date', 'is_current', 'description',
            'gpa', 'institution_logo', 'order'
        ]
    
    def get_start_date(self, obj):
        """Parse date string to extract start year as ISO date format"""
        date_str = obj.date or ''
        if 'Depuis' in date_str:
            year = date_str.replace('Depuis', '').strip()
            return f"{year}-01-01"
        if '–' in date_str:
            start = date_str.split('–')[0].strip()
            return f"{start}-01-01"
        if '-' in date_str and '–' not in date_str:
            start = date_str.split('-')[0].strip()
            return f"{start}-01-01"
        return f"{date_str.strip()}-01-01" if date_str else "2020-01-01"
    
    def get_end_date(self, obj):
        """Parse date string to extract end date"""
        date_str = obj.date or ''
        if 'Depuis' in date_str:
            return None
        if '–' in date_str:
            end = date_str.split('–')[1].strip()
            return f"{end}-01-01"
        if '-' in date_str and '–' not in date_str:
            parts = date_str.split('-')
            if len(parts) > 1:
                end = parts[1].strip()
                return f"{end}-01-01"
        return None
    
    def get_is_current(self, obj):
        """Check if this is a current education"""
        date_str = obj.date or ''
        return 'Depuis' in date_str or 'Present' in date_str or 'present' in date_str
    
    def get_description(self, obj):
        return ''  # Can be extended with a description field later
    
    def get_gpa(self, obj):
        return ''  # Can be extended with a gpa field later
    
    def get_institution_logo(self, obj):
        return None  # Can be extended with a logo field later


class ProjectBulletSerializer(serializers.ModelSerializer):
    """Serializer for project bullet points"""
    
    class Meta:
        model = ProjectBullet
        fields = ['id', 'text', 'order']


class ExperienceBulletSerializer(serializers.ModelSerializer):
    """Serializer for experience bullet points"""
    
    class Meta:
        model = ExperienceBullet
        fields = ['id', 'text', 'order']


class ExperienceSerializer(serializers.ModelSerializer):
    """Serializer for work experience - maps to frontend Experience type"""
    bullets = ExperienceBulletSerializer(many=True, read_only=True)
    position = serializers.CharField(source='title', read_only=True)
    company_logo = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Experience
        fields = [
            'id', 'position', 'company', 'company_url', 'location',
            'start_date', 'end_date', 'is_current',
            'description', 'bullets', 'company_logo', 'order'
        ]
    
    def get_company_logo(self, obj):
        return None  # Can be extended later with actual logo field
    
    def get_start_date(self, obj):
        """Convert start_date to ISO format"""
        date_str = obj.start_date or ''
        # If it's already in ISO format, return as is
        if len(date_str) == 10 and '-' in date_str:
            return date_str
        # Otherwise, try to parse month year format
        return f"{date_str}-01-01" if date_str else None
    
    def get_end_date(self, obj):
        """Convert end_date to ISO format"""
        if obj.is_current or not obj.end_date:
            return None
        date_str = obj.end_date
        # If it's already in ISO format, return as is
        if len(date_str) == 10 and '-' in date_str:
            return date_str
        # Otherwise, try to parse month year format
        return f"{date_str}-01-01" if date_str else None


class CertificationSerializer(serializers.ModelSerializer):
    """Serializer for certifications - maps to frontend Certification type"""
    issue_date = serializers.SerializerMethodField()
    expiry_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Certification
        fields = [
            'id', 'name', 'issuing_organization', 'issue_date',
            'expiry_date', 'credential_id', 'credential_url',
            'description', 'order'
        ]
    
    def get_issue_date(self, obj):
        """Convert issue_date to ISO format"""
        date_str = obj.issue_date or ''
        if len(date_str) == 10 and '-' in date_str:
            return date_str
        return f"{date_str}-01-01" if date_str else None
    
    def get_expiry_date(self, obj):
        """Convert expiry_date to ISO format"""
        if not obj.expiry_date:
            return None
        date_str = obj.expiry_date
        if len(date_str) == 10 and '-' in date_str:
            return date_str
        return f"{date_str}-01-01" if date_str else None


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for languages - maps to frontend Language type"""
    proficiency = serializers.CharField(source='get_proficiency_display', read_only=True)
    
    class Meta:
        model = Language
        fields = ['id', 'name', 'proficiency', 'order']


class InterestSerializer(serializers.ModelSerializer):
    """Serializer for interests"""
    
    class Meta:
        model = Interest
        fields = ['id', 'name', 'icon', 'order']


class CustomSectionItemSerializer(serializers.ModelSerializer):
    """Serializer for custom section items"""
    
    class Meta:
        model = CustomSectionItem
        fields = [
            'id', 'title', 'subtitle', 'description',
            'date', 'url', 'icon', 'order'
        ]


class CustomSectionSerializer(serializers.ModelSerializer):
    """Serializer for custom sections with nested items"""
    items = CustomSectionItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = CustomSection
        fields = [
            'id', 'title', 'slug', 'icon', 'content',
            'order', 'show_in_nav', 'items'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the main profile - maps to frontend Profile type"""
    full_name = serializers.CharField(source='name', read_only=True)
    title = serializers.CharField(source='hero_title', read_only=True)
    subtitle = serializers.CharField(source='hero_subtitle', read_only=True)
    short_bio = serializers.CharField(source='bio_short', read_only=True)
    avatar = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()
    is_available_for_hire = serializers.SerializerMethodField()
    social_links = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'full_name', 'title', 'subtitle',
            'email', 'phone', 'location',
            'avatar', 'bio', 'short_bio', 'resume',
            'is_available_for_hire', 'social_links',
            'show_blog', 'show_projects', 'show_contact',
            'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']
    
    def get_avatar(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None
    
    def get_resume(self, obj):
        if obj.resume:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.resume.url)
            return obj.resume.url
        return None
    
    def get_is_available_for_hire(self, obj):
        return True  # Can be extended with actual field later
    
    def get_social_links(self, obj):
        """Include social links in profile response"""
        from .models import SocialLink
        links = SocialLink.objects.filter(is_active=True)
        return SocialLinkSerializer(links, many=True).data


class PortfolioProjectSerializer(serializers.ModelSerializer):
    """Serializer for projects in the portfolio context"""
    bullets = ProjectBulletSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    technologies = serializers.SerializerMethodField()
    featured_image = serializers.SerializerMethodField()
    live_url = serializers.URLField(source='project_url', read_only=True)
    is_published = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description', 'description',
            'featured_image', 'technologies',
            'tags', 'live_url', 'github_url',
            'is_featured', 'is_published', 'bullets', 'order', 'created_at'
        ]
    
    def get_technologies(self, obj):
        return [tech.strip() for tech in obj.technologies_used.split(',') if tech.strip()]
    
    def get_featured_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def get_is_published(self, obj):
        return obj.status == 'published'


class PortfolioSerializer(serializers.Serializer):
    """
    Main serializer that combines all portfolio content for the frontend.
    Returns all data needed to render the entire portfolio in one API call.
    """
    profile = ProfileSerializer(read_only=True)
    skills = SkillGroupSerializer(many=True, read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    interests = InterestSerializer(many=True, read_only=True)
    projects = PortfolioProjectSerializer(many=True, read_only=True)
    custom_sections = CustomSectionSerializer(many=True, read_only=True)