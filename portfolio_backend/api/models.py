from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from PIL import Image
import os


class Category(models.Model):
    """Model representing a blog category"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Model representing a tag"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    """Model representing a portfolio project with SEO and optimization"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True, default='')
    description = models.TextField()
    short_description = models.CharField(
        max_length=300,
        help_text="Brief description for preview cards",
        default="No description provided."
    )
    image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    thumbnail = models.ImageField(
        upload_to='projects/thumbnails/',
        blank=True,
        null=True,
        editable=False
    )
    technologies_used = models.CharField(
        max_length=300,
        help_text="Comma-separated list, e.g., 'Django, TypeScript, CSS'"
    )
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)
    project_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=70, blank=True, default='')
    meta_description = models.CharField(max_length=160, blank=True, default='')
    
    # Status and ordering
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    is_featured = models.BooleanField(default=False, db_index=True)
    order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    views_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['-is_featured', 'order']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Set meta fields if not provided
        if not self.meta_title:
            self.meta_title = self.title[:70]
        if not self.meta_description:
            self.meta_description = self.short_description[:160]
        
        super().save(*args, **kwargs)
        
        # Create thumbnail after saving
        if self.image:
            self.create_thumbnail()

    def create_thumbnail(self):
        """Create optimized thumbnail from main image"""
        if not self.image:
            return
        
        try:
            img = Image.open(self.image.path)
            
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Create thumbnail
            img.thumbnail((400, 300), Image.Resampling.LANCZOS)
            
            # Generate thumbnail path
            thumb_name = f"thumb_{os.path.basename(self.image.name)}"
            thumb_path = os.path.join(
                os.path.dirname(self.image.path).replace('projects', 'projects/thumbnails'),
                thumb_name
            )
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
            
            # Save thumbnail
            img.save(thumb_path, 'JPEG', quality=85, optimize=True)
            
            # Update thumbnail field
            self.thumbnail = f"projects/thumbnails/{thumb_name}"
            Project.objects.filter(pk=self.pk).update(thumbnail=self.thumbnail)
        except Exception as e:
            print(f"Error creating thumbnail: {e}")

    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class BlogPost(models.Model):
    """Model representing a blog post with full SEO and optimization"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True, max_length=200, db_index=True)
    excerpt = models.CharField(
        max_length=300,
        help_text="Brief summary for previews and SEO",
        default="No excerpt provided."
    )
    content = models.TextField()
    featured_image = models.ImageField(
        upload_to='blog/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    
    # Relationships
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_posts'
    )
    tags = models.ManyToManyField(Tag, related_name='blog_posts', blank=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=70, blank=True, default='')
    meta_description = models.CharField(max_length=160, blank=True, default='')
    
    # Status and metrics
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False, db_index=True)
    views_count = models.IntegerField(default=0)
    reading_time = models.IntegerField(
        default=5,
        help_text="Estimated reading time in minutes"
    )
    
    published_date = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['status', '-published_date']),
            models.Index(fields=['-is_featured', '-published_date']),
            models.Index(fields=['slug']),
            models.Index(fields=['author', '-published_date']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug and calculate reading time"""
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Set meta fields if not provided
        if not self.meta_title:
            self.meta_title = self.title[:70]
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]
        
        # Calculate reading time (average 200 words per minute)
        word_count = len(self.content.split())
        self.reading_time = max(1, word_count // 200)
        
        super().save(*args, **kwargs)

    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class ContactSubmission(models.Model):
    """Model representing a contact form submission"""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(db_index=True)
    subject = models.CharField(max_length=200, default="General Inquiry")
    message = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    
    # Admin notes
    admin_notes = models.TextField(blank=True)
    
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['status', '-submitted_at']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class Subscriber(models.Model):
    """Model for newsletter subscribers"""
    email = models.EmailField(unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Singleton model for global site data and hero section"""
    # Basic Info
    name = models.CharField(max_length=100, default='Djousse Tedongmene Alex')
    hero_title = models.CharField(
        max_length=200, 
        default='Futur Actuaire & Data Scientist',
        help_text="Main headline displayed in the hero section"
    )
    hero_subtitle = models.CharField(
        max_length=300, 
        blank=True,
        help_text="Optional subtitle below the main headline"
    )
    
    # Contact Info
    email = models.EmailField(default='alextedongmene@gmail.com')
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=100, default='7011 Ghlin, Belgique')
    
    # Profile Images
    profile_image = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Main profile/avatar image"
    )
    hero_background = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Background image for hero section"
    )
    
    # About Section
    bio = models.TextField(
        default="Étudiant en Master Sciences Actuarielles (ULB)...",
        help_text="Main bio/about text"
    )
    bio_short = models.CharField(
        max_length=300,
        blank=True,
        help_text="Short bio for previews and meta descriptions"
    )
    
    # Resume/CV
    resume = models.FileField(
        upload_to='profile/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        help_text="Upload your resume/CV file"
    )
    
    # Legacy field (kept for backward compatibility)
    github_url = models.URLField(default='https://github.com/aldjoted', blank=True)
    
    # SEO Fields
    meta_title = models.CharField(
        max_length=70, 
        blank=True,
        help_text="SEO title for the website"
    )
    meta_description = models.CharField(
        max_length=160, 
        blank=True,
        help_text="SEO description for the website"
    )
    
    # Settings
    show_blog = models.BooleanField(default=True, help_text="Show blog section")
    show_projects = models.BooleanField(default=True, help_text="Show projects section")
    show_contact = models.BooleanField(default=True, help_text="Show contact form")
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def save(self, *args, **kwargs):
        if not self.pk and Profile.objects.exists():
            raise ValidationError('There can be only one Profile instance')
        
        # Set meta fields if not provided
        if not self.meta_title:
            self.meta_title = self.name
        if not self.meta_description:
            self.meta_description = self.bio_short or self.bio[:160]
        
        return super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Education(models.Model):
    """Model for education timeline"""
    date = models.CharField(max_length=50, help_text="e.g. 'Depuis 2025' or '2021–2025'")
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, help_text="Institution name")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Education"

    def __str__(self):
        return self.title


class SkillGroup(models.Model):
    """Model for skill categories"""
    title = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=100, 
        blank=True,
        default='fas fa-code',
        help_text="FontAwesome icon class, e.g., 'fas fa-code'"
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class SkillItem(models.Model):
    """Model for specific skills within a group"""
    group = models.ForeignKey(SkillGroup, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(
        default=0,
        help_text="Proficiency level from 0 to 100"
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class ProjectBullet(models.Model):
    """Model for bullet points in project details"""
    project = models.ForeignKey(Project, related_name='bullets', on_delete=models.CASCADE)
    text = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:50]


class SocialLink(models.Model):
    """Model for social media links"""
    ICON_CHOICES = [
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter/X'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('dribbble', 'Dribbble'),
        ('behance', 'Behance'),
        ('medium', 'Medium'),
        ('dev', 'Dev.to'),
        ('stackoverflow', 'Stack Overflow'),
        ('codepen', 'CodePen'),
        ('discord', 'Discord'),
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('website', 'Website'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    url = models.URLField()
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='website')
    custom_icon_class = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Custom FontAwesome class, e.g., 'fab fa-spotify'"
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return self.name


class Experience(models.Model):
    """Model for work/professional experience"""
    title = models.CharField(max_length=200, help_text="Job title")
    company = models.CharField(max_length=200)
    company_url = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.CharField(max_length=50, help_text="e.g., 'Jan 2023' or '2023'")
    end_date = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Leave blank for current position"
    )
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-is_current']
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"

    def __str__(self):
        return f"{self.title} at {self.company}"


class ExperienceBullet(models.Model):
    """Model for bullet points in experience details"""
    experience = models.ForeignKey(
        Experience, 
        related_name='bullets', 
        on_delete=models.CASCADE
    )
    text = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:50]


class Certification(models.Model):
    """Model for certifications and awards"""
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.CharField(max_length=50, help_text="e.g., 'Dec 2024' or '2024'")
    expiry_date = models.CharField(max_length=50, blank=True)
    credential_id = models.CharField(max_length=200, blank=True)
    credential_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"

    def __str__(self):
        return self.name


class Language(models.Model):
    """Model for language proficiency"""
    PROFICIENCY_CHOICES = [
        ('native', 'Native / Bilingual'),
        ('fluent', 'Fluent'),
        ('advanced', 'Advanced'),
        ('intermediate', 'Intermediate'),
        ('beginner', 'Beginner'),
    ]
    
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return f"{self.name} ({self.get_proficiency_display()})"


class Interest(models.Model):
    """Model for personal interests and hobbies"""
    name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=100, 
        blank=True,
        help_text="FontAwesome icon class, e.g., 'fas fa-music'"
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Interest"
        verbose_name_plural = "Interests"

    def __str__(self):
        return self.name


class CustomSection(models.Model):
    """Model for creating custom dynamic sections"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    icon = models.CharField(
        max_length=100, 
        blank=True,
        help_text="FontAwesome icon class, e.g., 'fas fa-star'"
    )
    content = models.TextField(
        blank=True,
        help_text="Rich text content (supports HTML)"
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    show_in_nav = models.BooleanField(
        default=True, 
        help_text="Show this section in navigation"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Custom Section"
        verbose_name_plural = "Custom Sections"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class CustomSectionItem(models.Model):
    """Model for items within a custom section"""
    section = models.ForeignKey(
        CustomSection, 
        related_name='items', 
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    date = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Custom Section Item"
        verbose_name_plural = "Custom Section Items"

    def __str__(self):
        return self.title