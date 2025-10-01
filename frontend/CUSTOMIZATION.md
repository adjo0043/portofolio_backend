# Quick Customization Guide

## 🎨 Personalize Your Portfolio

### 1. Update Personal Information

**In `index.html`:**

```html
<!-- Line 57: Update name -->
<span class="name typing-text" id="typing-text">Your Name</span>

<!-- Line 61: Update role -->
<span class="subtitle-text">Full-Stack Developer</span>

<!-- Line 67: Update description -->
<p class="hero-description">
    Crafting elegant solutions to complex problems with clean code and creative thinking
</p>

<!-- Line 84: Update social links -->
<a href="https://github.com/YOUR_USERNAME" target="_blank">
<a href="https://linkedin.com/in/YOUR_USERNAME" target="_blank">
<a href="https://twitter.com/YOUR_USERNAME" target="_blank">
<a href="mailto:YOUR_EMAIL@example.com">

<!-- Line 106: Update about text -->
<p class="lead">Your personal bio here...</p>

<!-- Line 199: Update contact information -->
<a href="mailto:your@email.com">your@email.com</a>
<a href="tel:+1234567890">+1 (234) 567-890</a>
<p>Your City, Country</p>
```

### 2. Update Avatar Image

**Replace placeholder avatar:**
```html
<!-- Line 48 in index.html -->
<img src="path/to/your/photo.jpg" alt="Your Name" class="avatar-img">
```

Or use a service like:
- Gravatar: `https://www.gravatar.com/avatar/YOUR_HASH?s=200`
- UIAvatars: `https://ui-avatars.com/api/?name=Your+Name&size=200`

### 3. Change Color Scheme

**In `style.css` (lines 4-11):**
```css
:root {
    --primary-color: #667eea;      /* Main brand color */
    --secondary-color: #764ba2;     /* Secondary brand color */
    --accent-color: #f093fb;        /* Accent highlights */
}
```

**Popular color schemes:**

**Blue & Purple (Current)**
```css
--primary-color: #667eea;
--secondary-color: #764ba2;
--accent-color: #f093fb;
```

**Green & Teal**
```css
--primary-color: #10b981;
--secondary-color: #14b8a6;
--accent-color: #34d399;
```

**Orange & Pink**
```css
--primary-color: #f97316;
--secondary-color: #ec4899;
--accent-color: #fb923c;
```

**Blue & Cyan**
```css
--primary-color: #3b82f6;
--secondary-color: #06b6d4;
--accent-color: #60a5fa;
```

### 4. Add Your Projects

**Replace mock data in `src/main.ts` (around line 329):**
```typescript
{
    id: 1,
    title: 'Your Project Name',
    description: 'Brief description of your project',
    image: 'https://your-image-url.com/project.jpg',
    technologies_used: 'React, Node.js, MongoDB',
    project_url: 'https://your-project.com',
    github_url: 'https://github.com/you/project',
    status: 'completed', // or 'inprogress' or 'featured'
    category: 'web' // or 'mobile' or 'api'
}
```

### 5. Add Your Blog Posts

**In `src/main.ts` (around line 433):**
```typescript
{
    id: 1,
    title: 'Your Blog Post Title',
    slug: 'your-blog-post-slug',
    content: 'Your blog post content here...',
    author_name: 'Your Name',
    published_date: '2025-01-01',
    category: 'Tutorial', // or 'Frontend', 'Backend', etc.
    read_time: 5 // minutes
}
```

### 6. Update CV Download

**In `src/main.ts` (around line 746):**
```typescript
const cvUrl = '/path/to/your/cv.pdf';
link.download = 'YourName_CV.pdf';
```

Place your CV file in the frontend folder or use an external URL.

### 7. Change Fonts

**In `index.html` (line 11):**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">
```

**Popular font combinations:**
- **Professional**: Inter + Poppins (Current)
- **Modern**: Outfit + Space Grotesk
- **Classic**: Lora + Source Sans Pro
- **Bold**: Montserrat + Open Sans
- **Elegant**: Playfair Display + Lato

Update CSS variables after changing fonts:
```css
--font-primary: 'Inter', sans-serif;
--font-heading: 'Poppins', sans-serif;
```

### 8. Customize Statistics

**In `index.html` (lines 113-135):**
```html
<div class="stat-number" data-target="50">0</div>
<div class="stat-label">Projects Completed</div>
```

Change the `data-target` value to your actual numbers.

### 9. Update Timeline

**In `index.html` (lines 155-184):**
```html
<div class="timeline-item">
    <div class="timeline-dot"></div>
    <div class="timeline-content">
        <span class="timeline-date">2022 - Present</span>
        <h4>Your Job Title</h4>
        <p>Brief description of your role</p>
    </div>
</div>
```

### 10. Modify Skills

**In `index.html` (lines 140-151):**
```html
<span class="skill-tag backend">Your Skill</span>
```

Classes available: `backend`, `frontend`, `database`, `tools`

### 11. Connect to Your Backend

**In `src/main.ts` (line 2):**
```typescript
const API_BASE_URL = 'http://localhost:8000/api';
```

Change to your production API URL when deploying.

### 12. Update Footer

**In `index.html` (lines 280-320):**
```html
<p>&copy; 2025 Your Name. All rights reserved.</p>
<p>Designed & Built with <i class="fas fa-heart"></i> by Your Name</p>
```

## 🎯 Quick Wins

### Remove Mock Data
Once your backend is working, remove the mock data fallback:
```typescript
// In src/main.ts, remove these lines:
if (allProjects.length === 0) {
    allProjects = getMockProjects();
}
```

### Add Google Analytics
```html
<!-- Add before </head> in index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Add Favicon
Replace `favicon.ico` with your own icon, or add this to `<head>`:
```html
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
```

### SEO Optimization
```html
<!-- Add these meta tags in <head> -->
<meta name="description" content="Your Name - Full-Stack Developer Portfolio">
<meta name="keywords" content="your, keywords, here">
<meta name="author" content="Your Name">

<!-- Open Graph for social sharing -->
<meta property="og:title" content="Your Name - Portfolio">
<meta property="og:description" content="Your professional description">
<meta property="og:image" content="https://your-site.com/og-image.jpg">
<meta property="og:url" content="https://your-site.com">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:creator" content="@your_twitter">
```

## 🚀 Deployment Checklist

- [ ] Update all personal information
- [ ] Replace mock data with real content
- [ ] Add your projects and blog posts
- [ ] Update social media links
- [ ] Add your CV file
- [ ] Change API URL to production
- [ ] Test on multiple devices
- [ ] Check all links work
- [ ] Optimize images
- [ ] Add favicon
- [ ] Add analytics
- [ ] Add meta tags for SEO
- [ ] Test form submission
- [ ] Build TypeScript: `npm run build`
- [ ] Deploy to hosting service

## 📱 Testing Checklist

- [ ] Desktop Chrome
- [ ] Desktop Firefox
- [ ] Desktop Safari
- [ ] Mobile Chrome
- [ ] Mobile Safari
- [ ] Tablet view
- [ ] Dark mode works
- [ ] All links open correctly
- [ ] Form validation works
- [ ] Contact form submits
- [ ] Scroll animations smooth
- [ ] Navigation highlights correctly
- [ ] Modal opens and closes
- [ ] Project filters work
- [ ] Blog search works
- [ ] Keyboard navigation works
- [ ] Screen reader friendly

---

Need help? Check the main README.md for detailed documentation!
