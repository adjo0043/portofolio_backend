from django.contrib import admin
from django.utils.html import format_html
from .models import Project, BlogPost, ContactSubmission, Category, Tag, Subscriber


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model"""
    list_display = ['name', 'slug', 'post_count', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def post_count(self, obj):
        return obj.blog_posts.count()
    post_count.short_description = 'Number of Posts'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for Tag model"""
    list_display = ['name', 'slug', 'usage_count', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def usage_count(self, obj):
        return obj.projects.count() + obj.blog_posts.count()
    usage_count.short_description = 'Total Usage'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for Project model"""
    list_display = [
        'title',
        'status',
        'is_featured',
        'views_count',
        'order',
        'image_preview',
        'created_at'
    ]
    list_filter = ['status', 'is_featured', 'created_at', 'tags']
    search_fields = ['title', 'description', 'technologies_used']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['thumbnail', 'views_count', 'created_at', 'updated_at', 'image_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Media', {
            'fields': ('image', 'thumbnail', 'image_preview')
        }),
        ('Technical Details', {
            'fields': ('technologies_used', 'tags')
        }),
        ('Links', {
            'fields': ('project_url', 'github_url', 'demo_url')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status & Ordering', {
            'fields': ('status', 'is_featured', 'order', 'views_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.thumbnail.url
            )
        elif obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Admin interface for BlogPost model"""
    list_display = [
        'title',
        'author',
        'category',
        'status',
        'is_featured',
        'views_count',
        'reading_time',
        'published_date'
    ]
    list_filter = ['status', 'is_featured', 'category', 'tags', 'published_date']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['reading_time', 'views_count', 'published_date', 'updated_at', 'image_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Media', {
            'fields': ('featured_image', 'image_preview')
        }),
        ('Classification', {
            'fields': ('author', 'category', 'tags')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status & Metrics', {
            'fields': ('status', 'is_featured', 'views_count', 'reading_time')
        }),
        ('Timestamps', {
            'fields': ('published_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.featured_image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'
    
    def save_model(self, request, obj, form, change):
        """Set author to current user if not set"""
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """Admin interface for ContactSubmission model"""
    list_display = [
        'name',
        'email',
        'subject',
        'status',
        'submitted_at',
        'ip_address'
    ]
    list_filter = ['status', 'submitted_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'phone', 'ip_address', 'user_agent', 'submitted_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('status', 'admin_notes')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'submitted_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Disable adding contact submissions through admin"""
        return False


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """Admin interface for Subscriber model"""
    list_display = ['email', 'is_active', 'subscribed_at', 'unsubscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['email', 'subscribed_at', 'unsubscribed_at']
    
    actions = ['deactivate_subscribers']
    
    def deactivate_subscribers(self, request, queryset):
        """Bulk deactivate subscribers"""
        from django.utils import timezone
        count = queryset.update(is_active=False, unsubscribed_at=timezone.now())
        self.message_user(request, f'{count} subscriber(s) deactivated.')
    deactivate_subscribers.short_description = 'Deactivate selected subscribers'


# Customize admin site
admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin Portal"
admin.site.index_title = "Welcome to Portfolio Administration"
