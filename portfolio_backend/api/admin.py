from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Project, BlogPost, ContactSubmission, Category, Tag, Subscriber,
    Profile, Education, SkillGroup, SkillItem, ProjectBullet,
    SocialLink, Experience, ExperienceBullet, Certification,
    Language, Interest, CustomSection, CustomSectionItem
)


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


class ProjectBulletInline(admin.TabularInline):
    model = ProjectBullet
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for Project model"""
    inlines = [ProjectBulletInline]
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


class SkillItemInline(admin.TabularInline):
    model = SkillItem
    extra = 1


@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    inlines = [SkillItemInline]
    list_display = ('title', 'order')
    ordering = ('order',)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'date', 'order')
    ordering = ('order',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Profile (singleton)"""
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'hero_title', 'hero_subtitle')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Images', {
            'fields': ('profile_image', 'hero_background', 'profile_preview')
        }),
        ('About', {
            'fields': ('bio', 'bio_short')
        }),
        ('Resume/CV', {
            'fields': ('resume',),
            'classes': ('collapse',)
        }),
        ('Legacy Social Links', {
            'fields': ('github_url',),
            'classes': ('collapse',),
            'description': 'Use the Social Links section for managing all social links.'
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Site Settings', {
            'fields': ('show_blog', 'show_projects', 'show_contact')
        }),
    )
    
    readonly_fields = ['profile_preview', 'updated_at']
    
    def profile_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="max-height: 150px; border-radius: 50%;" />',
                obj.profile_image.url
            )
        return "No image"
    profile_preview.short_description = 'Profile Preview'
    
    def has_add_permission(self, request):
        # Only allow one Profile instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the profile
        return False


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """Admin interface for Social Links"""
    list_display = ['name', 'icon', 'url_preview', 'order', 'is_active']
    list_filter = ['icon', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'url']
    ordering = ['order']
    
    fieldsets = (
        ('Link Information', {
            'fields': ('name', 'url', 'icon')
        }),
        ('Custom Icon', {
            'fields': ('custom_icon_class',),
            'classes': ('collapse',),
            'description': 'Use this for icons not in the dropdown (e.g., fab fa-spotify)'
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def url_preview(self, obj):
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">{}</a>',
            obj.url,
            obj.url[:40] + '...' if len(obj.url) > 40 else obj.url
        )
    url_preview.short_description = 'URL'


class ExperienceBulletInline(admin.TabularInline):
    model = ExperienceBullet
    extra = 2
    ordering = ['order']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """Admin interface for Work Experience"""
    inlines = [ExperienceBulletInline]
    list_display = ['title', 'company', 'date_display', 'is_current', 'order', 'is_active']
    list_filter = ['is_current', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'company', 'description']
    ordering = ['order', '-is_current']
    
    fieldsets = (
        ('Position', {
            'fields': ('title', 'company', 'company_url')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'is_current'),
            'description': 'Leave end date blank for current positions'
        }),
        ('Details', {
            'fields': ('location', 'description')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def date_display(self, obj):
        if obj.is_current:
            return f"{obj.start_date} – Present"
        elif obj.end_date:
            return f"{obj.start_date} – {obj.end_date}"
        return obj.start_date
    date_display.short_description = 'Period'


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    """Admin interface for Certifications"""
    list_display = ['name', 'issuing_organization', 'issue_date', 'has_url', 'order', 'is_active']
    list_filter = ['is_active', 'issuing_organization']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'issuing_organization']
    ordering = ['order']
    
    fieldsets = (
        ('Certification', {
            'fields': ('name', 'issuing_organization')
        }),
        ('Dates', {
            'fields': ('issue_date', 'expiry_date')
        }),
        ('Credentials', {
            'fields': ('credential_id', 'credential_url'),
            'classes': ('collapse',)
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def has_url(self, obj):
        return bool(obj.credential_url)
    has_url.boolean = True
    has_url.short_description = 'Has Link'


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """Admin interface for Languages"""
    list_display = ['name', 'proficiency', 'order', 'is_active']
    list_filter = ['proficiency', 'is_active']
    list_editable = ['proficiency', 'order', 'is_active']
    ordering = ['order']


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    """Admin interface for Interests"""
    list_display = ['name', 'icon_display', 'order', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    ordering = ['order']
    
    def icon_display(self, obj):
        if obj.icon:
            return format_html('<i class="{}" style="font-size: 1.2em;"></i> {}', obj.icon, obj.icon)
        return '-'
    icon_display.short_description = 'Icon'


class CustomSectionItemInline(admin.StackedInline):
    model = CustomSectionItem
    extra = 1
    ordering = ['order']
    fieldsets = (
        (None, {
            'fields': (('title', 'subtitle'), ('date', 'url'), 'description', ('icon', 'order', 'is_active'))
        }),
    )


@admin.register(CustomSection)
class CustomSectionAdmin(admin.ModelAdmin):
    """Admin interface for Custom Sections"""
    inlines = [CustomSectionItemInline]
    list_display = ['title', 'slug', 'item_count', 'show_in_nav', 'order', 'is_active']
    list_filter = ['is_active', 'show_in_nav']
    list_editable = ['order', 'is_active', 'show_in_nav']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content']
    ordering = ['order']
    
    fieldsets = (
        ('Section Info', {
            'fields': ('title', 'slug', 'icon')
        }),
        ('Content', {
            'fields': ('content',),
            'description': 'Rich text content. Use HTML for formatting.'
        }),
        ('Display', {
            'fields': ('order', 'show_in_nav', 'is_active')
        }),
    )
    
    def item_count(self, obj):
        count = obj.items.count()
        return f"{count} item{'s' if count != 1 else ''}"
    item_count.short_description = 'Items'


# Customize admin site
admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin Portal"
admin.site.index_title = "Welcome to Portfolio Administration"
