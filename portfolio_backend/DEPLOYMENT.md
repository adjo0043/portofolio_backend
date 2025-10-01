# 🚀 Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Deployment Options](#deployment-options)
3. [Platform-Specific Guides](#platform-specific-guides)
4. [Post-Deployment](#post-deployment)

---

## Prerequisites

Before deploying, ensure you have:
- ✅ Generated a strong `SECRET_KEY`
- ✅ Set `DEBUG=False` in production
- ✅ Configured all environment variables
- ✅ Set up a PostgreSQL database
- ✅ Configured email service (SMTP/SendGrid)
- ✅ Domain name (optional but recommended)
- ✅ SSL certificate (Let's Encrypt recommended)

---

## Deployment Options

### 1. Traditional VPS (DigitalOcean, AWS EC2, Linode)
**Best for:** Full control, custom configurations
**Difficulty:** Moderate
**Cost:** $5-20/month

### 2. Platform as a Service (Heroku, Railway, Render)
**Best for:** Quick deployment, less maintenance
**Difficulty:** Easy
**Cost:** $7-25/month

### 3. Docker Containers (AWS ECS, Google Cloud Run)
**Best for:** Scalability, microservices
**Difficulty:** Moderate to Hard
**Cost:** Variable

### 4. Serverless (AWS Lambda with Zappa)
**Best for:** Low traffic, cost optimization
**Difficulty:** Moderate
**Cost:** Pay per use

---

## Platform-Specific Guides

## 🌊 Option 1: DigitalOcean Droplet

### Step 1: Create Droplet
```bash
# Choose: Ubuntu 22.04 LTS, 1GB RAM minimum
```

### Step 2: Initial Server Setup
```bash
# SSH into your server
ssh root@your_server_ip

# Create new user
adduser portfolio
usermod -aG sudo portfolio
su - portfolio

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx redis-server git
```

### Step 3: PostgreSQL Setup
```bash
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE portfolio_db;
CREATE USER portfolio_user WITH PASSWORD 'STRONG_PASSWORD_HERE';
ALTER ROLE portfolio_user SET client_encoding TO 'utf8';
ALTER ROLE portfolio_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE portfolio_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;
\q
```

### Step 4: Application Setup
```bash
# Create directory
sudo mkdir -p /var/www/portfolio
sudo chown portfolio:portfolio /var/www/portfolio
cd /var/www/portfolio

# Clone repository
git clone YOUR_REPO_URL .
cd portfolio_backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### Step 5: Environment Configuration
```bash
# Copy example env
cp .env.example .env

# Edit environment file
nano .env
```

**Production .env:**
```env
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your_server_ip

CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database
DB_NAME=portfolio_db
DB_USER=portfolio_user
DB_PASSWORD=STRONG_PASSWORD_HERE
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://127.0.0.1:6379/1

# Email (Gmail example)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
CONTACT_EMAIL=contact@yourdomain.com

THROTTLE_ANON=100/hour
THROTTLE_USER=1000/hour
TIME_ZONE=America/New_York
```

### Step 6: Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Step 7: Gunicorn Setup
```bash
# Test gunicorn
gunicorn --bind 0.0.0.0:8000 portfolio_backend.wsgi:application

# Create systemd service file
sudo nano /etc/systemd/system/portfolio.service
```

**Service file content:**
```ini
[Unit]
Description=Portfolio Django Application
After=network.target

[Service]
User=portfolio
Group=www-data
WorkingDirectory=/var/www/portfolio/portfolio_backend
Environment="PATH=/var/www/portfolio/portfolio_backend/venv/bin"
ExecStart=/var/www/portfolio/portfolio_backend/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/portfolio/portfolio_backend/portfolio.sock \
    --timeout 60 \
    --log-level info \
    --access-logfile /var/log/portfolio/access.log \
    --error-logfile /var/log/portfolio/error.log \
    portfolio_backend.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Create log directory
sudo mkdir -p /var/log/portfolio
sudo chown portfolio:www-data /var/log/portfolio

# Start and enable service
sudo systemctl start portfolio
sudo systemctl enable portfolio
sudo systemctl status portfolio
```

### Step 8: NGINX Configuration
```bash
sudo nano /etc/nginx/sites-available/portfolio
```

**NGINX config:**
```nginx
upstream portfolio_app {
    server unix:/var/www/portfolio/portfolio_backend/portfolio.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    client_max_body_size 10M;
    
    access_log /var/log/nginx/portfolio-access.log;
    error_log /var/log/nginx/portfolio-error.log;
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Static files
    location /static/ {
        alias /var/www/portfolio/portfolio_backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /var/www/portfolio/portfolio_backend/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    # API and admin
    location / {
        proxy_pass http://portfolio_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal test
sudo certbot renew --dry-run
```

### Step 10: Firewall Configuration
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

---

## 🚂 Option 2: Railway

### Step 1: Prepare for Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login
```

### Step 2: Create railway.json
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
  },
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT portfolio_backend.wsgi:application",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 3: Deploy
```bash
railway init
railway up
```

### Step 4: Add PostgreSQL and Redis
```bash
railway add --plugin postgresql
railway add --plugin redis
```

### Step 5: Environment Variables
Set in Railway dashboard:
- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS`
- All other env vars from `.env.example`

---

## 🟣 Option 3: Heroku

### Step 1: Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Create Procfile
```
web: gunicorn portfolio_backend.wsgi:application --log-file -
release: python manage.py migrate
```

### Step 3: Create runtime.txt
```
python-3.11.6
```

### Step 4: Deploy
```bash
heroku login
heroku create your-portfolio-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Add Redis
heroku addons:create heroku-redis:mini

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app.herokuapp.com"

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## 🐳 Option 4: Docker Deployment

### Step 1: Build Image
```bash
docker build -t portfolio-backend .
```

### Step 2: Push to Registry
```bash
# Docker Hub
docker tag portfolio-backend yourusername/portfolio-backend:latest
docker push yourusername/portfolio-backend:latest

# Or AWS ECR / Google Container Registry
```

### Step 3: Deploy with Docker Compose
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Step 4: AWS ECS Deployment
1. Create ECS cluster
2. Create task definition
3. Create service
4. Configure load balancer
5. Set environment variables in task definition

---

## Post-Deployment Checklist

### ✅ Security
- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] HTTPS/SSL enabled
- [ ] Firewall configured
- [ ] Database password is strong
- [ ] Admin URL is protected
- [ ] CORS properly configured
- [ ] Rate limiting enabled

### ✅ Performance
- [ ] Static files served via CDN or NGINX
- [ ] Database connection pooling enabled
- [ ] Redis cache configured
- [ ] Gzip compression enabled
- [ ] Database indexes created
- [ ] Query optimization verified

### ✅ Monitoring
- [ ] Error tracking (Sentry) configured
- [ ] Application logging enabled
- [ ] Health check endpoint working
- [ ] Uptime monitoring set up (UptimeRobot)
- [ ] Database backups automated

### ✅ Functionality
- [ ] Admin panel accessible
- [ ] API endpoints working
- [ ] Email notifications working
- [ ] Image uploads working
- [ ] Contact form working
- [ ] All migrations applied

---

## Maintenance Tasks

### Daily
- Monitor error logs
- Check health endpoint
- Review rate limit violations

### Weekly
- Database backup
- Check disk space
- Review slow queries
- Update dependencies (if needed)

### Monthly
- Security updates
- SSL certificate renewal check
- Performance review
- Database optimization

---

## Troubleshooting

### Issue: 500 Internal Server Error
```bash
# Check logs
sudo journalctl -u portfolio -n 50
tail -f /var/log/portfolio/error.log
```

### Issue: Static files not loading
```bash
python manage.py collectstatic --noinput
sudo systemctl restart portfolio
sudo systemctl restart nginx
```

### Issue: Database connection error
```bash
# Test database connection
python manage.py dbshell

# Check PostgreSQL status
sudo systemctl status postgresql
```

### Issue: Permission denied
```bash
# Fix ownership
sudo chown -R portfolio:www-data /var/www/portfolio
sudo chmod -R 755 /var/www/portfolio
```

---

## Useful Commands

```bash
# Restart application
sudo systemctl restart portfolio

# View logs
sudo journalctl -u portfolio -f

# Check NGINX config
sudo nginx -t

# Reload NGINX
sudo systemctl reload nginx

# Database backup
pg_dump -U portfolio_user portfolio_db > backup.sql

# Clear cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

---

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (NGINX, AWS ELB)
- Session storage in Redis
- Separate database server
- CDN for static/media files

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement connection pooling
- Use async views for I/O operations

---

**Deployment completed! 🎉**
