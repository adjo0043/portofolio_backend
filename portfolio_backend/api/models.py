from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Project(models.Model):
    """Model representing a portfolio project"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    technologies_used = models.CharField(
        max_length=300,
        help_text="Comma-separated list, e.g., 'Django, TypeScript, CSS'"
    )
    project_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    """Model representing a blog post"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    published_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ContactSubmission(models.Model):
    """Model representing a contact form submission"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Message from {self.name} at {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"