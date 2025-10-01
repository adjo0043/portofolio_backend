"""
Tests for Portfolio Backend API
"""
import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Project, BlogPost, ContactSubmission, Category, Tag


class ProjectAPITestCase(APITestCase):
    """Test cases for Project API"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test tags
        self.tag1 = Tag.objects.create(name="Django", slug="django")
        self.tag2 = Tag.objects.create(name="React", slug="react")
        
        # Create test projects
        self.project1 = Project.objects.create(
            title="Test Project 1",
            slug="test-project-1",
            description="Description for test project 1",
            short_description="Short description 1",
            technologies_used="Django, React",
            status="published",
            is_featured=True
        )
        self.project1.tags.add(self.tag1, self.tag2)
        
        self.project2 = Project.objects.create(
            title="Test Project 2",
            slug="test-project-2",
            description="Description for test project 2",
            short_description="Short description 2",
            technologies_used="Python, Flask",
            status="published",
            is_featured=False
        )
    
    def test_list_projects(self):
        """Test getting list of projects"""
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_get_project_detail(self):
        """Test getting single project"""
        response = self.client.get(f'/api/projects/{self.project1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Project 1')
    
    def test_filter_featured_projects(self):
        """Test filtering featured projects"""
        response = self.client.get('/api/projects/', {'is_featured': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_search_projects(self):
        """Test searching projects"""
        response = self.client.get('/api/projects/', {'search': 'Django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] >= 1)


class BlogPostAPITestCase(APITestCase):
    """Test cases for BlogPost API"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test category
        self.category = Category.objects.create(
            name="Technology",
            slug="technology",
            description="Tech articles"
        )
        
        # Create test posts
        self.post1 = BlogPost.objects.create(
            title="Test Post 1",
            slug="test-post-1",
            excerpt="Excerpt for test post 1",
            content="Content for test post 1. " * 50,  # Make it long enough
            author=self.user,
            category=self.category,
            status="published",
            is_featured=True
        )
        
        self.post2 = BlogPost.objects.create(
            title="Test Post 2",
            slug="test-post-2",
            excerpt="Excerpt for test post 2",
            content="Content for test post 2. " * 50,
            author=self.user,
            status="published"
        )
    
    def test_list_blog_posts(self):
        """Test getting list of blog posts"""
        response = self.client.get('/api/blog/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_get_blog_post_detail(self):
        """Test getting single blog post"""
        response = self.client.get(f'/api/blog/{self.post1.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post 1')
    
    def test_search_blog_posts(self):
        """Test searching blog posts"""
        response = self.client.get('/api/blog/search/', {'q': 'Test Post 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] >= 1)
    
    def test_filter_by_category(self):
        """Test filtering posts by category"""
        response = self.client.get('/api/blog/', {'category': 'technology'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)


class ContactAPITestCase(APITestCase):
    """Test cases for Contact API"""
    
    def setUp(self):
        """Set up test client"""
        self.client = APIClient()
    
    def test_submit_contact_form_valid(self):
        """Test submitting valid contact form"""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message with sufficient length.'
        }
        response = self.client.post('/api/contact/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
    
    def test_submit_contact_form_invalid_email(self):
        """Test submitting contact form with invalid email"""
        data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'subject': 'Test',
            'message': 'Test message'
        }
        response = self.client.post('/api/contact/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_submit_contact_form_short_message(self):
        """Test submitting contact form with short message"""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test',
            'message': 'Short'
        }
        response = self.client.post('/api/contact/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_submit_contact_form_spam_detection(self):
        """Test spam detection in contact form"""
        data = {
            'name': 'Spammer',
            'email': 'spam@example.com',
            'subject': 'Spam',
            'message': 'Check out http://spam1.com http://spam2.com http://spam3.com http://spam4.com'
        }
        response = self.client.post('/api/contact/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HealthCheckTestCase(APITestCase):
    """Test cases for Health Check endpoint"""
    
    def setUp(self):
        """Set up test client"""
        self.client = APIClient()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertIn('database', response.data)


class CategoryAPITestCase(APITestCase):
    """Test cases for Category API"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Web Development",
            slug="web-development",
            description="Web dev articles"
        )
    
    def test_list_categories(self):
        """Test getting list of categories"""
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)
    
    def test_get_category_detail(self):
        """Test getting single category"""
        response = self.client.get(f'/api/categories/{self.category.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Web Development')


class TagAPITestCase(APITestCase):
    """Test cases for Tag API"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.tag = Tag.objects.create(name="Python", slug="python")
    
    def test_list_tags(self):
        """Test getting list of tags"""
        response = self.client.get('/api/tags/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)


class ModelTestCase(TestCase):
    """Test cases for models"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_project_slug_generation(self):
        """Test automatic slug generation for projects"""
        project = Project.objects.create(
            title="My New Project",
            description="Description",
            short_description="Short desc",
            technologies_used="Django"
        )
        self.assertEqual(project.slug, "my-new-project")
    
    def test_blog_post_slug_generation(self):
        """Test automatic slug generation for blog posts"""
        post = BlogPost.objects.create(
            title="My New Blog Post",
            excerpt="Excerpt",
            content="Content " * 50,
            author=self.user
        )
        self.assertEqual(post.slug, "my-new-blog-post")
    
    def test_blog_post_reading_time(self):
        """Test reading time calculation"""
        # 400 words should be ~2 minutes
        content = " ".join(["word"] * 400)
        post = BlogPost.objects.create(
            title="Reading Time Test",
            excerpt="Excerpt",
            content=content,
            author=self.user
        )
        self.assertEqual(post.reading_time, 2)
    
    def test_category_slug_generation(self):
        """Test automatic slug generation for categories"""
        category = Category.objects.create(
            name="Web Development"
        )
        self.assertEqual(category.slug, "web-development")
    
    def test_tag_slug_generation(self):
        """Test automatic slug generation for tags"""
        tag = Tag.objects.create(name="Machine Learning")
        self.assertEqual(tag.slug, "machine-learning")


# Run tests with: python manage.py test
# Or with pytest: pytest
