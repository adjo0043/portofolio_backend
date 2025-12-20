# 🚀 Render.com Production Environment Checklist

This checklist documents all environment variables required to deploy the Portfolio application to Render.com.

---

## 📋 Deployment Overview

| Component | Service Type | Plan |
|-----------|-------------|------|
| Django Backend | Web Service | Starter+ |
| PostgreSQL | Database | Starter+ |
| Redis (Optional) | Redis | Starter+ |

---

## ✅ Required Environment Variables

### 🔐 Django Core Settings

| Variable | Required | Auto-Generated | Description |
|----------|----------|----------------|-------------|
| `SECRET_KEY` | ✅ Yes | ✅ Yes | Django secret key. Set `generateValue: true` in render.yaml |
| `DEBUG` | ✅ Yes | ❌ No | **Must be `False`** in production |
| `ALLOWED_HOSTS` | ✅ Yes | ✅ Partial | Auto-set from Render service hostname |

### 🗄️ Database Configuration

| Variable | Required | Auto-Generated | Description |
|----------|----------|----------------|-------------|
| `DATABASE_URL` | ✅ Yes | ✅ Yes | PostgreSQL connection string. Auto-linked from Render database |

**Example Format:** `postgres://user:password@host:5432/database_name`

### 🔄 Cache Configuration (Redis)

| Variable | Required | Auto-Generated | Description |
|----------|----------|----------------|-------------|
| `REDIS_URL` | ❌ Optional | ✅ Yes | Redis connection string. Falls back to local memory cache if not set |

**Note:** Redis requires a paid plan on Render. The app will work without it using local memory cache.

---

## 🌐 CORS & CSRF Settings

These **must be configured manually** in the Render Dashboard after deployment.

| Variable | Required | Example Value |
|----------|----------|---------------|
| `CORS_ALLOWED_ORIGINS` | ✅ Yes | `https://your-frontend.onrender.com,https://yourdomain.com` |
| `CSRF_TRUSTED_ORIGINS` | ✅ Yes | `https://your-frontend.onrender.com,https://yourdomain.com` |

**⚠️ Important:** 
- Include your frontend domain(s)
- Use HTTPS URLs only
- Separate multiple origins with commas (no spaces)

---

## 📧 Email Configuration

Configure these for contact form and notifications to work.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `EMAIL_BACKEND` | ❌ Optional | `django.core.mail.backends.smtp.EmailBackend` | Email backend class |
| `EMAIL_HOST` | ✅ For email | - | SMTP server (e.g., `smtp.gmail.com`) |
| `EMAIL_PORT` | ❌ Optional | `587` | SMTP port |
| `EMAIL_USE_TLS` | ❌ Optional | `True` | Enable TLS encryption |
| `EMAIL_HOST_USER` | ✅ For email | - | SMTP username/email |
| `EMAIL_HOST_PASSWORD` | ✅ For email | - | SMTP password or app password |
| `DEFAULT_FROM_EMAIL` | ❌ Optional | - | Default sender email |
| `CONTACT_EMAIL` | ❌ Optional | - | Email to receive contact form submissions |

### SendGrid Alternative
| Variable | Required | Description |
|----------|----------|-------------|
| `SENDGRID_API_KEY` | ❌ Optional | SendGrid API key for transactional emails |

---

## ⚡ Rate Limiting

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `THROTTLE_ANON` | ❌ Optional | `100/hour` | Rate limit for anonymous users |
| `THROTTLE_USER` | ❌ Optional | `1000/hour` | Rate limit for authenticated users |

---

## 🕐 Timezone & Logging

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TIME_ZONE` | ❌ Optional | `UTC` | Application timezone |
| `DJANGO_LOG_LEVEL` | ❌ Optional | `INFO` | Logging verbosity level |

---

## ☁️ AWS S3 Configuration (Optional)

For serving media files from S3 instead of local storage.

| Variable | Required | Description |
|----------|----------|-------------|
| `AWS_ACCESS_KEY_ID` | ❌ Optional | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | ❌ Optional | AWS secret key |
| `AWS_STORAGE_BUCKET_NAME` | ❌ Optional | S3 bucket name |
| `AWS_S3_REGION_NAME` | ❌ Optional | AWS region (default: `us-east-1`) |

---

## 🔔 Error Tracking (Optional)

| Variable | Required | Description |
|----------|----------|-------------|
| `SENTRY_DSN` | ❌ Optional | Sentry DSN for error tracking |

---

## 📝 Step-by-Step Deployment Guide

### 1. Create New Blueprint on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New** → **Blueprint**
3. Connect your GitHub/GitLab repository
4. Select the repository containing `render.yaml`
5. Click **Apply**

### 2. Configure Secret Environment Variables

After the initial deployment, go to your **Web Service** → **Environment**:

1. **Verify `SECRET_KEY`** was auto-generated
2. **Set `CORS_ALLOWED_ORIGINS`**:
   ```
   https://your-app-name.onrender.com
   ```
3. **Set `CSRF_TRUSTED_ORIGINS`**:
   ```
   https://your-app-name.onrender.com
   ```
4. **Configure Email** (if needed):
   - `EMAIL_HOST`: `smtp.gmail.com`
   - `EMAIL_HOST_USER`: `your-email@gmail.com`
   - `EMAIL_HOST_PASSWORD`: Your app password (not regular password)

### 3. Verify Database Connection

The `DATABASE_URL` is automatically injected from the linked PostgreSQL service.

### 4. Create Admin User (Optional)

After deployment, use the **Shell** tab in your Web Service:

```bash
python manage.py createsuperuser
```

### 5. Update Frontend API URL

Update `API_BASE_URL` in [frontend/src/main.ts](frontend/src/main.ts) to point to your Render backend:

```typescript
const API_BASE_URL = 'https://your-app-name.onrender.com/api';
```

Then rebuild and redeploy.

---

## 🔒 Security Checklist

Before going live, verify:

- [ ] `DEBUG` is set to `False`
- [ ] `SECRET_KEY` is a strong, unique value (auto-generated)
- [ ] `ALLOWED_HOSTS` includes only your domains
- [ ] `CORS_ALLOWED_ORIGINS` is restricted to your frontend domains
- [ ] `CSRF_TRUSTED_ORIGINS` matches your frontend domains
- [ ] HTTPS is enforced (automatic on Render)
- [ ] Database credentials are not exposed
- [ ] Sensitive environment variables are marked as "Secret" in Render

---

## 🐛 Troubleshooting

### "DisallowedHost" Error
Add your domain to `ALLOWED_HOSTS` environment variable.

### CORS Errors
Ensure `CORS_ALLOWED_ORIGINS` includes your frontend URL with the correct protocol (https://).

### Database Connection Failed
1. Check if the PostgreSQL database is running
2. Verify `DATABASE_URL` is correctly linked
3. Check database plan limits

### Static Files Not Loading
Ensure `collectstatic` ran during build. Check build logs for errors.

### 502 Bad Gateway
1. Check application logs for startup errors
2. Verify Gunicorn is starting correctly
3. Check if all dependencies are installed

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `render.yaml` | Render.com IaC blueprint defining all services |
| `portfolio_backend/build.sh` | Build script for dependency installation and asset compilation |
| `RENDER_DEPLOYMENT.md` | This checklist document |

---

## 🔗 Useful Links

- [Render.com Documentation](https://render.com/docs)
- [Django on Render](https://render.com/docs/deploy-django)
- [Render Environment Variables](https://render.com/docs/environment-variables)
- [Render Blueprints](https://render.com/docs/infrastructure-as-code)
