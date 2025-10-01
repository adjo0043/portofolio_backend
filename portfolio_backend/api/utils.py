"""
Utility functions for the API app
"""
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from PIL import Image
import os
import hashlib


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """Get user agent from request"""
    return request.META.get('HTTP_USER_AGENT', '')[:255]


def send_contact_email(contact_submission):
    """
    Send email notification for new contact submission
    """
    try:
        subject = f"New Contact Form Submission: {contact_submission.subject}"
        message = f"""
New contact form submission received:

Name: {contact_submission.name}
Email: {contact_submission.email}
Subject: {contact_submission.subject}
Phone: {contact_submission.phone or 'Not provided'}

Message:
{contact_submission.message}

Submitted at: {contact_submission.submitted_at}
IP Address: {contact_submission.ip_address or 'Unknown'}
        """
        
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.CONTACT_EMAIL]
        
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending contact email: {e}")
        return False


def send_welcome_email(subscriber_email):
    """
    Send welcome email to new newsletter subscriber
    """
    try:
        subject = "Welcome to Our Newsletter!"
        message = f"""
Thank you for subscribing to our newsletter!

You'll receive updates about new blog posts, projects, and more.

If you wish to unsubscribe, please visit our website.

Best regards,
Your Portfolio Team
        """
        
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [subscriber_email]
        
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending welcome email: {e}")
        return False


def optimize_image(image_path, max_size=(1920, 1080), quality=85):
    """
    Optimize image file size while maintaining quality
    
    Args:
        image_path: Path to the image file
        max_size: Maximum dimensions (width, height)
        quality: JPEG quality (1-100)
    """
    try:
        img = Image.open(image_path)
        
        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background
        
        # Resize if larger than max_size
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save optimized image
        img.save(image_path, 'JPEG', quality=quality, optimize=True)
        
        return True
    except Exception as e:
        print(f"Error optimizing image: {e}")
        return False


def create_cache_key(prefix, *args, **kwargs):
    """
    Create a consistent cache key from prefix and arguments
    
    Example:
        create_cache_key('projects', 'list', page=1, status='published')
    """
    parts = [str(prefix)]
    parts.extend(str(arg) for arg in args)
    parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    
    key_string = ':'.join(parts)
    
    # Hash if key is too long
    if len(key_string) > 200:
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        return f"{prefix}:{key_hash}"
    
    return key_string


def invalidate_cache_pattern(pattern):
    """
    Invalidate all cache keys matching a pattern
    
    Note: This works with Redis backend. For other backends,
    you might need to track keys separately.
    """
    try:
        if hasattr(cache, 'delete_pattern'):
            cache.delete_pattern(f"*{pattern}*")
            return True
    except Exception as e:
        print(f"Error invalidating cache pattern: {e}")
    return False


def calculate_reading_time(text, words_per_minute=200):
    """
    Calculate estimated reading time for text
    
    Args:
        text: Text content
        words_per_minute: Average reading speed
    
    Returns:
        Reading time in minutes
    """
    word_count = len(text.split())
    reading_time = max(1, word_count // words_per_minute)
    return reading_time


def sanitize_filename(filename):
    """
    Sanitize filename to prevent security issues
    """
    import re
    # Remove any non-alphanumeric characters except dots, hyphens, and underscores
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    # Remove multiple underscores
    filename = re.sub(r'_+', '_', filename)
    return filename


def validate_image_file(file):
    """
    Validate uploaded image file
    
    Returns:
        (is_valid, error_message)
    """
    # Check file size (max 5MB)
    max_size = 5 * 1024 * 1024
    if file.size > max_size:
        return False, "Image file size cannot exceed 5MB"
    
    # Check file extension
    allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
    ext = file.name.split('.')[-1].lower()
    if ext not in allowed_extensions:
        return False, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
    
    # Try to open as image
    try:
        img = Image.open(file)
        img.verify()
        return True, None
    except Exception as e:
        return False, "Invalid image file"


def generate_meta_description(text, max_length=160):
    """
    Generate a meta description from text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    if len(text) <= max_length:
        return text
    
    # Truncate at word boundary
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > 0:
        truncated = truncated[:last_space]
    
    return truncated + '...'


class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded"""
    pass


def check_rate_limit(identifier, limit=10, period=60):
    """
    Check if rate limit is exceeded for an identifier
    
    Args:
        identifier: Unique identifier (e.g., IP address)
        limit: Maximum number of requests
        period: Time period in seconds
    
    Returns:
        Boolean indicating if limit is exceeded
    """
    cache_key = f"rate_limit:{identifier}"
    
    try:
        current = cache.get(cache_key, 0)
        
        if current >= limit:
            return True
        
        cache.set(cache_key, current + 1, period)
        return False
    except Exception:
        # If cache fails, allow the request
        return False
