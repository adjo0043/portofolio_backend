# Portfolio Backend API

🚀 **High-Performance, Production-Ready Django REST API** for modern portfolio websites.

## ✨ Features

### Core Functionality
- ✅ **Projects API** - Full CRUD with image handling and optimization
- ✅ **Blog System** - Categories, tags, search, and SEO optimization
- ✅ **Contact Forms** - With email notifications and spam protection
- ✅ **Newsletter** - Subscriber management
- ✅ **Admin Interface** - Easy content management

### Performance & Optimization
- ⚡ **Database Optimization** - Proper indexing, select_related, prefetch_related
- 🚀 **Caching Strategy** - Redis/LocMem with intelligent cache invalidation
- 📄 **Pagination** - Efficient handling of large datasets
- 🔍 **Advanced Search** - Full-text search across models
- 🗜️ **Response Compression** - Gzip compression for API responses
- 🖼️ **Image Optimization** - Automatic thumbnail generation and compression

### Security Features
- 🔒 **CORS Protection** - Configurable allowed origins
- 🛡️ **CSRF Protection** - Built-in Django CSRF
- 🚦 **Rate Limiting** - Per-IP throttling (100 req/hour for anon users)
- ✅ **Input Validation** - Comprehensive sanitization
- 🔐 **SQL Injection Prevention** - Django ORM protection
- 🔑 **Secure Headers** - HSTS, XSS protection, content type sniffing

### Production Ready
- 🐳 **Docker Support** - Complete containerization
- 📊 **Health Checks** - Monitoring endpoints
- 📝 **Structured Logging** - Rotating file logs
- 🌐 **NGINX Configuration** - Reverse proxy and static file serving
- 🔄 **Database Migrations** - Version controlled schema changes

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Performance Tuning](#performance-tuning)
- [Contributing](#contributing)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip
- virtualenv (recommended)
- PostgreSQL (for production)
- Redis (optional, for caching)

### Local Development Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd portfolio_backend
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Generate secret key**
```bash
python generate_secret_key.py
```

6. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```

8. **Collect static files**
```bash
python manage.py collectstatic
```

9. **Run development server**
```bash
python manage.py runserver
```

Visit: `http://localhost:8000/api/` to see the API
Admin: `http://localhost:8000/admin/`

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Endpoints

#### 📁 Projects

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/projects/` | List all published projects | No |
| GET | `/api/projects/{slug}/` | Get single project | No |
| GET | `/api/projects/featured/` | Get featured projects | No |
| GET | `/api/projects/technologies/` | List all technologies | No |

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 10, max: 100)
- `status` - Filter by status (published, draft, archived)
- `is_featured` - Filter featured (true/false)
- `tags` - Filter by tag slug
- `search` - Search in title, description, technologies

**Example Response:**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/projects/?page=2",
  "previous": null,
  "total_pages": 2,
  "current_page": 1,
  "results": [
    {
      "id": 1,
      "title": "E-Commerce Platform",
      "slug": "e-commerce-platform",
      "short_description": "Full-featured online store",
      "thumbnail": "/media/projects/thumbnails/thumb_ecommerce.jpg",
      "technology_list": ["Django", "React", "PostgreSQL"],
      "tags": [
        {"id": 1, "name": "Web Development", "slug": "web-development"}
      ],
      "project_url": "https://example.com",
      "github_url": "https://github.com/...",
      "is_featured": true,
      "views_count": 150,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

#### 📝 Blog Posts

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/blog/` | List all published posts | No |
| GET | `/api/blog/{slug}/` | Get single post | No |
| GET | `/api/blog/featured/` | Get featured posts | No |
| GET | `/api/blog/search/?q=query` | Search posts | No |

**Query Parameters:**
- `page`, `page_size` - Pagination
- `status` - Filter by status
- `category` - Filter by category slug
- `tags` - Filter by tag slug
- `author` - Filter by author username
- `search` - Full-text search

**Example Response:**
```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "title": "Getting Started with Django",
      "slug": "getting-started-with-django",
      "excerpt": "Learn the basics of Django framework",
      "featured_image": "/media/blog/django-intro.jpg",
      "author_name": "John Doe",
      "category_name": "Tutorials",
      "tags": [
        {"id": 1, "name": "Django", "slug": "django"}
      ],
      "is_featured": true,
      "views_count": 250,
      "reading_time": 5,
      "published_date": "2024-01-20T14:00:00Z"
    }
  ]
}
```

---

#### 📧 Contact Form

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/contact/` | Submit contact form | No |

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Inquiry about services",
  "message": "I would like to discuss...",
  "phone": "+1234567890"  // optional
}
```

**Response:**
```json
{
  "message": "Thank you for your message! We will get back to you soon.",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Inquiry about services",
    "message": "I would like to discuss...",
    "submitted_at": "2024-01-20T15:30:00Z"
  }
}
```

**Rate Limiting:** 10 submissions per hour per IP

---

#### 📰 Newsletter

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/subscribe/` | Subscribe to newsletter | No |

**Request Body:**
```json
{
  "email": "subscriber@example.com"
}
```

---

#### 🏷️ Categories & Tags

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/categories/` | List all categories | No |
| GET | `/api/categories/{slug}/` | Get category details | No |
| GET | `/api/tags/` | List all tags | No |
| GET | `/api/tags/{slug}/` | Get tag details | No |

---

#### 💚 Health Check

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/health/` | System health status | No |

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "cache": "connected",
  "timestamp": "now"
}
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Django Core
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com

# Database (PostgreSQL)
DB_NAME=portfolio_db
DB_USER=portfolio_user
DB_PASSWORD=secure-password
DB_HOST=localhost
DB_PORT=5432

# Redis Cache
REDIS_URL=redis://127.0.0.1:6379/1

# Email (SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
CONTACT_EMAIL=contact@yourdomain.com

# Rate Limiting
THROTTLE_ANON=100/hour
THROTTLE_USER=1000/hour
```

---

## 🐳 Docker Deployment

### Development with Docker

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Stop services
docker-compose down
```

### Production with Docker

```bash
# Build for production
docker-compose -f docker-compose.prod.yml up -d

# Scale web workers
docker-compose -f docker-compose.prod.yml up -d --scale web=3
```

---

## 🚀 Production Deployment

### 1. Server Setup (Ubuntu/Debian)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx redis-server

# Create database
sudo -u postgres psql
CREATE DATABASE portfolio_db;
CREATE USER portfolio_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;
\q
```

### 2. Application Setup

```bash
# Clone repository
cd /var/www
git clone <your-repo> portfolio

# Set up virtual environment
cd portfolio/portfolio_backend
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with production values

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

### 3. Gunicorn Setup

Create `/etc/systemd/system/portfolio.service`:

```ini
[Unit]
Description=Portfolio Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/portfolio/portfolio_backend
Environment="PATH=/var/www/portfolio/portfolio_backend/venv/bin"
ExecStart=/var/www/portfolio/portfolio_backend/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/var/www/portfolio/portfolio_backend/portfolio.sock \
    --timeout 60 \
    --access-logfile /var/log/portfolio/access.log \
    --error-logfile /var/log/portfolio/error.log \
    portfolio_backend.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Create log directory
sudo mkdir -p /var/log/portfolio
sudo chown www-data:www-data /var/log/portfolio

# Start service
sudo systemctl start portfolio
sudo systemctl enable portfolio
sudo systemctl status portfolio
```

### 4. NGINX Configuration

Create `/etc/nginx/sites-available/portfolio`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    client_max_body_size 10M;
    
    location /static/ {
        alias /var/www/portfolio/portfolio_backend/staticfiles/;
        expires 30d;
    }
    
    location /media/ {
        alias /var/www/portfolio/portfolio_backend/media/;
        expires 7d;
    }
    
    location / {
        proxy_pass http://unix:/var/www/portfolio/portfolio_backend/portfolio.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## ⚡ Performance Tuning

### Database Optimization

1. **Use PostgreSQL in production**
2. **Enable connection pooling**
3. **Add proper indexes** (already configured in models)
4. **Use database query optimization**:
   - `select_related()` for foreign keys
   - `prefetch_related()` for many-to-many
   - `only()` / `defer()` for field selection

### Caching Strategy

1. **Install Redis**:
```bash
pip install django-redis redis hiredis
```

2. **Update settings.py**:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

3. **Cache usage**:
- API responses (15-30 minutes)
- Database queries
- Template fragments

### Image Optimization

Images are automatically optimized on upload:
- Thumbnails generated (400x300)
- JPEG quality: 85%
- Maximum size: 1920x1080

For better performance, consider:
- **CDN integration** (AWS S3, Cloudflare)
- **WebP format** conversion
- **Lazy loading** on frontend

---

## 📊 Monitoring & Logging

### Application Logs

Logs are stored in `/logs/` directory (or `/var/log/portfolio/` in production).

View logs:
```bash
tail -f logs/django.log
```

### Database Monitoring

```bash
# Check database size
python manage.py dbshell
SELECT pg_size_pretty(pg_database_size('portfolio_db'));

# Check slow queries
python manage.py shell
from django.db import connection
print(connection.queries)
```

### Performance Monitoring

Install Django Debug Toolbar (development only):
```python
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=api --cov-report=html

# Specific test file
pytest api/tests/test_models.py
```

---

## 📝 API Rate Limits

| Endpoint | Rate Limit |
|----------|-----------|
| `/api/projects/` | 100 req/hour (anonymous) |
| `/api/blog/` | 100 req/hour (anonymous) |
| `/api/contact/` | 10 req/hour per IP |
| `/api/subscribe/` | 5 req/hour per IP |

Authenticated users: 1000 req/hour

---

## 🔧 Maintenance

### Backup Database

```bash
# PostgreSQL
pg_dump -U portfolio_user portfolio_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U portfolio_user portfolio_db < backup_20240120.sql
```

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart portfolio
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 📞 Support

For support, email contact@yourdomain.com or open an issue on GitHub.

---

## 🙏 Acknowledgments

- Django REST Framework
- PostgreSQL
- Redis
- Docker
- NGINX

---

**Built with ❤️ for high-performance portfolio websites**
