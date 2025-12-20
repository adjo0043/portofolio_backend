from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    BlogPostViewSet,
    ContactSubmissionViewSet,
    CategoryViewSet,
    TagViewSet,
    SubscriberViewSet,
    HealthCheckViewSet,
    PortfolioView,
    ProfileView,
    SkillsView,
    EducationView,
    ExperienceView,
    SocialLinksView
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'blog', BlogPostViewSet, basename='blogpost')
router.register(r'contact', ContactSubmissionViewSet, basename='contact')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'subscribe', SubscriberViewSet, basename='subscriber')
router.register(r'health', HealthCheckViewSet, basename='health')

urlpatterns = [
    path('', include(router.urls)),
    # Portfolio content endpoints
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('skills/', SkillsView.as_view(), name='skills'),
    path('education/', EducationView.as_view(), name='education'),
    path('experience/', ExperienceView.as_view(), name='experience'),
    path('social-links/', SocialLinksView.as_view(), name='social-links'),
]