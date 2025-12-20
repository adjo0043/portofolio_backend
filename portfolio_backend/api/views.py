from rest_framework import viewsets, mixins, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from django.core.cache import cache
from django.db.models import Q, Prefetch
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Project, BlogPost, ContactSubmission, Category, Tag, Subscriber,
    Profile, Education, SkillGroup, SkillItem, ProjectBullet,
    SocialLink, Experience, ExperienceBullet, Certification,
    Language, Interest, CustomSection, CustomSectionItem
)
from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    ContactSubmissionSerializer,
    CategorySerializer,
    TagSerializer,
    SubscriberSerializer,
    ProfileSerializer,
    EducationSerializer,
    SkillGroupSerializer,
    SocialLinkSerializer,
    ExperienceSerializer,
    CertificationSerializer,
    LanguageSerializer,
    InterestSerializer,
    CustomSectionSerializer,
    PortfolioProjectSerializer,
    PortfolioSerializer
)
from .pagination import StandardResultsSetPagination, LargeResultsSetPagination
from .filters import ProjectFilter, BlogPostFilter, ContactSubmissionFilter
from .utils import (
    get_client_ip,
    get_user_agent,
    send_contact_email,
    send_welcome_email,
    create_cache_key,
    check_rate_limit,
    RateLimitExceeded
)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing projects with optimization and caching
    
    Endpoints:
    - GET /api/projects/ - List all published projects
    - GET /api/projects/{slug}/ - Get single project details
    - GET /api/projects/featured/ - Get featured projects
    """
    queryset = Project.objects.select_related().prefetch_related('tags')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['title', 'description', 'technologies_used']
    ordering_fields = ['created_at', 'views_count', 'order']
    ordering = ['-is_featured', 'order', '-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectListSerializer
    
    def get_queryset(self):
        """Optimize queryset and filter by status"""
        queryset = super().get_queryset()
        
        # Only show published projects to non-authenticated users
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        
        return queryset
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        """List projects with caching"""
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Get single project and increment view count"""
        instance = self.get_object()
        
        # Increment view count (don't cache this)
        instance.increment_views()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured projects"""
        cache_key = create_cache_key('projects', 'featured')
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        queryset = self.get_queryset().filter(is_featured=True)[:6]
        serializer = self.get_serializer(queryset, many=True)
        
        cache.set(cache_key, serializer.data, 60 * 30)  # Cache for 30 minutes
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def technologies(self, request):
        """Get list of all unique technologies used"""
        cache_key = create_cache_key('projects', 'technologies')
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        projects = self.get_queryset().filter(status='published')
        all_techs = set()
        
        for project in projects:
            techs = [tech.strip() for tech in project.technologies_used.split(',') if tech.strip()]
            all_techs.update(techs)
        
        technologies = sorted(list(all_techs))
        cache.set(cache_key, technologies, 60 * 60)  # Cache for 1 hour
        
        return Response(technologies)


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing blog posts with optimization and caching
    
    Endpoints:
    - GET /api/blog/ - List all published blog posts
    - GET /api/blog/{slug}/ - Get single blog post details
    - GET /api/blog/featured/ - Get featured blog posts
    - GET /api/blog/search/?q=query - Search blog posts
    """
    queryset = BlogPost.objects.select_related('author', 'category').prefetch_related('tags')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BlogPostFilter
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['published_date', 'views_count', 'reading_time']
    ordering = ['-published_date']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostListSerializer
    
    def get_queryset(self):
        """Optimize queryset and filter by status"""
        queryset = super().get_queryset()
        
        # Only show published posts to non-authenticated users
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        
        return queryset
    
    @method_decorator(cache_page(60 * 10))  # Cache for 10 minutes
    def list(self, request, *args, **kwargs):
        """List blog posts with caching"""
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Get single blog post and increment view count"""
        instance = self.get_object()
        
        # Increment view count
        instance.increment_views()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured blog posts"""
        cache_key = create_cache_key('blog', 'featured')
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        queryset = self.get_queryset().filter(is_featured=True)[:6]
        serializer = self.get_serializer(queryset, many=True)
        
        cache.set(cache_key, serializer.data, 60 * 30)  # Cache for 30 minutes
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search across blog posts"""
        query = request.query_params.get('q', '')
        
        if not query:
            return Response({'results': [], 'count': 0})
        
        cache_key = create_cache_key('blog', 'search', q=query)
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        queryset = self.get_queryset().filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()[:20]
        
        serializer = self.get_serializer(queryset, many=True)
        result = {
            'results': serializer.data,
            'count': len(serializer.data),
            'query': query
        }
        
        cache.set(cache_key, result, 60 * 15)  # Cache for 15 minutes
        return Response(result)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing blog categories
    
    Endpoints:
    - GET /api/categories/ - List all categories
    - GET /api/categories/{slug}/ - Get category details
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = 'slug'
    
    @method_decorator(cache_page(60 * 30))  # Cache for 30 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 30))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing tags
    
    Endpoints:
    - GET /api/tags/ - List all tags
    - GET /api/tags/{slug}/ - Get tag details
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = LargeResultsSetPagination
    lookup_field = 'slug'
    
    @method_decorator(cache_page(60 * 30))  # Cache for 30 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ContactSubmissionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for creating contact submissions with rate limiting
    
    Endpoints:
    - POST /api/contact/ - Submit contact form
    """
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Handle contact form submission with rate limiting"""
        # Get client IP for rate limiting
        client_ip = get_client_ip(request)
        
        # Check rate limit (10 submissions per hour)
        if check_rate_limit(f"contact:{client_ip}", limit=10, period=3600):
            return Response(
                {'error': 'Too many requests. Please try again later.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        # Validate and save
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Add IP and user agent
        contact = serializer.save(
            ip_address=client_ip,
            user_agent=get_user_agent(request)
        )
        
        # Send email notification (async in production)
        try:
            send_contact_email(contact)
        except Exception as e:
            print(f"Error sending email: {e}")
        
        return Response(
            {
                'message': 'Thank you for your message! We will get back to you soon.',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class SubscriberViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for newsletter subscriptions
    
    Endpoints:
    - POST /api/subscribe/ - Subscribe to newsletter
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Handle newsletter subscription"""
        # Get client IP for rate limiting
        client_ip = get_client_ip(request)
        
        # Check rate limit
        if check_rate_limit(f"subscribe:{client_ip}", limit=5, period=3600):
            return Response(
                {'error': 'Too many subscription attempts. Please try again later.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscriber = serializer.save()
        
        # Send welcome email
        try:
            send_welcome_email(subscriber.email)
        except Exception as e:
            print(f"Error sending welcome email: {e}")
        
        return Response(
            {
                'message': 'Successfully subscribed to newsletter!',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )


@method_decorator(cache_page(60 * 5), name='dispatch')
class HealthCheckViewSet(viewsets.ViewSet):
    """
    Health check endpoint for monitoring
    
    Endpoints:
    - GET /api/health/ - Get system health status
    """
    permission_classes = [AllowAny]
    
    def list(self, request):
        """Return health status"""
        from django.db import connection
        
        status_data = {
            'status': 'healthy',
            'database': 'connected',
            'cache': 'connected',
            'timestamp': cache.get('health_check_time', 'unknown')
        }
        
        # Check database
        try:
            connection.ensure_connection()
        except Exception as e:
            status_data['database'] = f'error: {str(e)}'
            status_data['status'] = 'unhealthy'
        
        # Check cache
        try:
            cache.set('health_check_time', 'now', 60)
            cache.get('health_check_time')
        except Exception as e:
            status_data['cache'] = f'error: {str(e)}'
            status_data['status'] = 'degraded'
        
        return Response(status_data)


class PortfolioView(APIView):
    """
    Main API endpoint that returns all portfolio content in a single request.
    This is optimized for the frontend to load all data at once.
    
    Endpoints:
    - GET /api/portfolio/ - Get complete portfolio data
    """
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def get(self, request):
        """Return all portfolio data"""
        cache_key = create_cache_key('portfolio', 'full')
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        # Get or create profile
        profile = Profile.objects.first()
        
        # Gather all portfolio data with optimized queries
        data = {
            'profile': ProfileSerializer(
                profile, 
                context={'request': request}
            ).data if profile else None,
            
            'skills': SkillGroupSerializer(
                SkillGroup.objects.prefetch_related('items'),
                many=True
            ).data,
            
            'education': EducationSerializer(
                Education.objects.all(),
                many=True
            ).data,
            
            'experiences': ExperienceSerializer(
                Experience.objects.filter(is_active=True).prefetch_related('bullets'),
                many=True
            ).data,
            
            'certifications': CertificationSerializer(
                Certification.objects.filter(is_active=True),
                many=True
            ).data,
            
            'languages': LanguageSerializer(
                Language.objects.filter(is_active=True),
                many=True
            ).data,
            
            'interests': InterestSerializer(
                Interest.objects.filter(is_active=True),
                many=True
            ).data,
            
            'projects': PortfolioProjectSerializer(
                Project.objects.filter(status='published')
                    .prefetch_related('bullets', 'tags')
                    .order_by('-is_featured', 'order', '-created_at'),
                many=True,
                context={'request': request}
            ).data,
            
            'custom_sections': CustomSectionSerializer(
                CustomSection.objects.filter(is_active=True)
                    .prefetch_related('items'),
                many=True
            ).data,
        }
        
        cache.set(cache_key, data, 60 * 5)  # Cache for 5 minutes
        return Response(data)


class ProfileView(APIView):
    """
    API endpoint for profile data only
    
    Endpoints:
    - GET /api/profile/ - Get profile data
    """
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(60 * 10))  # Cache for 10 minutes
    def get(self, request):
        """Return profile data"""
        profile = Profile.objects.first()
        if not profile:
            return Response({'detail': 'Profile not configured'}, status=404)
        
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)


class SkillsView(APIView):
    """
    API endpoint for skills data
    
    Endpoints:
    - GET /api/skills/ - Get all skill groups with items
    """
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def get(self, request):
        """Return skills data"""
        skills = SkillGroup.objects.prefetch_related('items').all()
        serializer = SkillGroupSerializer(skills, many=True)
        return Response(serializer.data)


class EducationView(APIView):
    """
    API endpoint for education data
    
    Endpoints:
    - GET /api/education/ - Get all education entries
    """
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def get(self, request):
        """Return education data"""
        education = Education.objects.all()
        serializer = EducationSerializer(education, many=True)
        return Response(serializer.data)


class ExperienceView(APIView):
    """
    API endpoint for experience data
    
    Endpoints:
    - GET /api/experience/ - Get all experience entries
    """
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def get(self, request):
        """Return experience data"""
        experience = Experience.objects.filter(is_active=True).prefetch_related('bullets')
        serializer = ExperienceSerializer(experience, many=True)
        return Response(serializer.data)


class SocialLinksView(APIView):
    """
    API endpoint for social links
    
    Endpoints:
    - GET /api/social-links/ - Get all social links
    """
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def get(self, request):
        """Return social links"""
        links = SocialLink.objects.filter(is_active=True)
        serializer = SocialLinkSerializer(links, many=True)
        return Response(serializer.data)