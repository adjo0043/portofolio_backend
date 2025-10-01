// API Base URL
const API_BASE_URL = 'http://localhost:8000/api';

// Type definitions
interface Project {
    id: number;
    title: string;
    description: string;
    image: string | null;
    technologies_used: string;
    project_url: string | null;
    github_url: string | null;
    created_at: string;
    updated_at: string;
    status?: 'completed' | 'inprogress' | 'featured';
    category?: string;
}

interface BlogPost {
    id: number;
    title: string;
    slug: string;
    content: string;
    author: number;
    author_name: string;
    published_date: string;
    updated_at: string;
    category?: string;
    read_time?: number;
}

interface ContactFormData {
    name: string;
    email: string;
    message: string;
    subject?: string;
}

interface ApiResponse<T> {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: T[];
}

// State management
let allProjects: Project[] = [];
let allBlogPosts: BlogPost[] = [];
let currentProjectFilter = 'all';
let currentBlogCategory = 'all';
let isLoadingProjects = false;
let isLoadingBlogs = false;

// Utility function to format date
function formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Calculate read time (average 200 words per minute)
function calculateReadTime(content: string): number {
    const words = content.trim().split(/\s+/).length;
    return Math.ceil(words / 200);
}

// Debounce function for search
function debounce<T extends (...args: any[]) => any>(
    func: T,
    wait: number
): (...args: Parameters<T>) => void {
    let timeout: number | undefined;
    return function(this: any, ...args: Parameters<T>) {
        clearTimeout(timeout);
        timeout = window.setTimeout(() => func.apply(this, args), wait);
    };
}

// Intersection Observer for scroll animations
function setupScrollAnimations(): void {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Progress bar on scroll
function updateProgressBar(): void {
    const progressBar = document.getElementById('progress-bar');
    if (!progressBar) return;

    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight - windowHeight;
    const scrolled = window.scrollY;
    const progress = (scrolled / documentHeight) * 100;
    
    progressBar.style.width = `${progress}%`;
}

// Back to top button
function setupBackToTop(): void {
    const backToTopBtn = document.getElementById('back-to-top');
    if (!backToTopBtn) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Navbar scroll effect
function setupNavbarScroll(): void {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const currentScroll = window.scrollY;
        
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });
}

// Active section highlighting
function setupActiveSection(): void {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = (section as HTMLElement).offsetTop;
            const sectionHeight = (section as HTMLElement).clientHeight;
            
            if (window.scrollY >= sectionTop - 100) {
                current = section.getAttribute('id') || '';
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('data-section') === current) {
                link.classList.add('active');
            }
        });
    });
}

// Mobile menu toggle
function setupMobileMenu(): void {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    
    if (!hamburger || !navMenu) return;

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    });

    // Close menu when clicking a link
    const navLinks = navMenu.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        const target = e.target as HTMLElement;
        if (!hamburger.contains(target) && !navMenu.contains(target)) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

// Dark mode toggle
function setupDarkMode(): void {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

    // Check for saved theme preference
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);

    themeToggle.addEventListener('click', () => {
        const theme = document.documentElement.getAttribute('data-theme');
        const newTheme = theme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
}

function updateThemeIcon(theme: string): void {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

    const icon = themeToggle.querySelector('i');
    if (!icon) return;

    icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
}

// Animated counter for stats
function animateCounter(element: HTMLElement): void {
    const target = parseInt(element.getAttribute('data-target') || '0');
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;

    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.ceil(current).toString();
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target.toString();
        }
    };

    updateCounter();
}

function setupCounters(): void {
    const counters = document.querySelectorAll('.stat-number[data-target]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && entry.target.textContent === '0') {
                animateCounter(entry.target as HTMLElement);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

// Typing effect for hero
function setupTypingEffect(): void {
    const typingElement = document.getElementById('typing-text');
    if (!typingElement) return;

    const texts = ['Your Name', 'Full-Stack Developer', 'Problem Solver', 'Tech Enthusiast'];
    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function type() {
        if (!typingElement) return;
        
        const currentText = texts[textIndex];
        
        if (isDeleting) {
            typingElement.textContent = currentText.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typingElement.textContent = currentText.substring(0, charIndex + 1);
            charIndex++;
        }

        let typeSpeed = isDeleting ? 50 : 100;

        if (!isDeleting && charIndex === currentText.length) {
            typeSpeed = 2000;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            textIndex = (textIndex + 1) % texts.length;
            typeSpeed = 500;
        }

        setTimeout(type, typeSpeed);
    }

    type();
}

// Fetch projects from API
async function fetchProjects(): Promise<void> {
    const projectsList = document.getElementById('projects-list');
    if (!projectsList || isLoadingProjects) return;

    isLoadingProjects = true;

    try {
        const response = await fetch(`${API_BASE_URL}/projects/`);
        if (!response.ok) {
            throw new Error('Failed to fetch projects');
        }

        const data: ApiResponse<Project> = await response.json();
        allProjects = data.results || [];

        // Add some mock data for demo purposes if no projects
        if (allProjects.length === 0) {
            allProjects = getMockProjects();
        }

        // Clear loading skeleton
        projectsList.innerHTML = '';

        if (allProjects.length === 0) {
            projectsList.innerHTML = '<p class="loading">No projects available yet.</p>';
            return;
        }

        renderProjects(allProjects);
    } catch (error) {
        console.error('Error fetching projects:', error);
        // Use mock data on error
        allProjects = getMockProjects();
        renderProjects(allProjects);
    } finally {
        isLoadingProjects = false;
    }
}

// Mock projects for demonstration
function getMockProjects(): Project[] {
    return [
        {
            id: 1,
            title: 'E-Commerce Platform',
            description: 'A full-featured e-commerce platform with cart, checkout, and payment integration.',
            image: 'https://via.placeholder.com/400x240/667eea/ffffff?text=E-Commerce',
            technologies_used: 'Django, React, PostgreSQL, Stripe',
            project_url: 'https://example.com',
            github_url: 'https://github.com',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            status: 'completed',
            category: 'web'
        },
        {
            id: 2,
            title: 'Task Management App',
            description: 'Collaborative task management application with real-time updates and team features.',
            image: 'https://via.placeholder.com/400x240/764ba2/ffffff?text=Task+Manager',
            technologies_used: 'TypeScript, Node.js, MongoDB, WebSocket',
            project_url: null,
            github_url: 'https://github.com',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            status: 'inprogress',
            category: 'web'
        },
        {
            id: 3,
            title: 'Weather API Service',
            description: 'RESTful API service providing weather data with caching and rate limiting.',
            image: 'https://via.placeholder.com/400x240/f093fb/ffffff?text=Weather+API',
            technologies_used: 'Python, FastAPI, Redis, Docker',
            project_url: 'https://example.com',
            github_url: 'https://github.com',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            status: 'featured',
            category: 'api'
        }
    ];
}

// Render projects
function renderProjects(projects: Project[]): void {
    const projectsList = document.getElementById('projects-list');
    if (!projectsList) return;

    projectsList.innerHTML = '';

    const filteredProjects = currentProjectFilter === 'all' 
        ? projects 
        : projects.filter(p => p.category === currentProjectFilter);

    if (filteredProjects.length === 0) {
        projectsList.innerHTML = '<p class="loading">No projects found in this category.</p>';
        return;
    }

    filteredProjects.forEach(project => {
        const projectCard = createProjectCard(project);
        projectsList.appendChild(projectCard);
    });
}

// Create a project card element
function createProjectCard(project: Project): HTMLElement {
    const card = document.createElement('div');
    card.className = 'project-card animate-on-scroll';
    card.setAttribute('data-project-id', project.id.toString());

    // Status badge
    if (project.status) {
        const statusBadge = document.createElement('span');
        statusBadge.className = `project-status status-${project.status}`;
        statusBadge.textContent = project.status === 'inprogress' ? 'In Progress' : project.status;
        card.appendChild(statusBadge);
    }

    // Image container
    const imageContainer = document.createElement('div');
    imageContainer.className = 'project-image-container';
    
    const imageUrl = project.image || `https://via.placeholder.com/400x240/667eea/ffffff?text=${encodeURIComponent(project.title)}`;
    const img = document.createElement('img');
    img.src = imageUrl;
    img.alt = project.title;
    img.className = 'project-image';
    img.loading = 'lazy';
    
    imageContainer.appendChild(img);
    card.appendChild(imageContainer);

    // Content container
    const content = document.createElement('div');
    content.className = 'project-content';

    // Title
    const title = document.createElement('h3');
    title.textContent = project.title;
    content.appendChild(title);

    // Description
    const description = document.createElement('p');
    description.textContent = project.description;
    content.appendChild(description);

    // Technologies
    const techContainer = document.createElement('div');
    techContainer.className = 'project-tech';
    const techList = project.technologies_used.split(',').map(t => t.trim());
    techList.forEach(tech => {
        const techTag = document.createElement('span');
        techTag.className = 'tech-tag';
        techTag.textContent = tech;
        techContainer.appendChild(techTag);
    });
    content.appendChild(techContainer);

    // Links
    const links = document.createElement('div');
    links.className = 'project-links';

    if (project.project_url) {
        const projectLink = document.createElement('a');
        projectLink.href = project.project_url;
        projectLink.target = '_blank';
        projectLink.rel = 'noopener noreferrer';
        projectLink.innerHTML = '<i class="fas fa-external-link-alt"></i> Live Demo';
        links.appendChild(projectLink);
    }

    if (project.github_url) {
        const githubLink = document.createElement('a');
        githubLink.href = project.github_url;
        githubLink.target = '_blank';
        githubLink.rel = 'noopener noreferrer';
        githubLink.innerHTML = '<i class="fab fa-github"></i> Code';
        links.appendChild(githubLink);
    }

    content.appendChild(links);
    card.appendChild(content);

    // Add click event to open modal
    card.addEventListener('click', (e) => {
        const target = e.target as HTMLElement;
        if (!target.closest('a')) {
            openProjectModal(project);
        }
    });

    return card;
}

// Project filtering
function setupProjectFilters(): void {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            currentProjectFilter = button.getAttribute('data-filter') || 'all';
            renderProjects(allProjects);
            setupScrollAnimations(); // Re-setup animations for new elements
        });
    });
}

// Project modal
function openProjectModal(project: Project): void {
    const modal = document.getElementById('project-modal');
    const modalBody = document.getElementById('modal-body');
    
    if (!modal || !modalBody) return;

    modalBody.innerHTML = `
        <div class="modal-project">
            <img src="${project.image || 'https://via.placeholder.com/800x400'}" 
                 alt="${project.title}" 
                 style="width: 100%; border-radius: 12px; margin-bottom: 24px;">
            <h2>${project.title}</h2>
            <p style="font-size: 1.125rem; line-height: 1.8; margin-bottom: 24px;">${project.description}</p>
            
            <div style="margin-bottom: 24px;">
                <h3>Technologies Used</h3>
                <div class="project-tech">
                    ${project.technologies_used.split(',').map(tech => 
                        `<span class="tech-tag">${tech.trim()}</span>`
                    ).join('')}
                </div>
            </div>
            
            <div class="project-links">
                ${project.project_url ? `
                    <a href="${project.project_url}" target="_blank" rel="noopener noreferrer" class="btn btn-primary">
                        <i class="fas fa-external-link-alt"></i> View Live
                    </a>
                ` : ''}
                ${project.github_url ? `
                    <a href="${project.github_url}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary">
                        <i class="fab fa-github"></i> View Code
                    </a>
                ` : ''}
            </div>
        </div>
    `;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function setupProjectModal(): void {
    const modal = document.getElementById('project-modal');
    const closeBtn = document.getElementById('modal-close');
    const overlay = document.getElementById('modal-overlay');

    if (!modal || !closeBtn || !overlay) return;

    const closeModal = () => {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    };

    closeBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', closeModal);

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
}

// Fetch blog posts from API
async function fetchBlogPosts(): Promise<void> {
    const blogPostsList = document.getElementById('blog-posts-list');
    if (!blogPostsList || isLoadingBlogs) return;

    isLoadingBlogs = true;

    try {
        const response = await fetch(`${API_BASE_URL}/blog/`);
        if (!response.ok) {
            throw new Error('Failed to fetch blog posts');
        }

        const data: ApiResponse<BlogPost> = await response.json();
        allBlogPosts = data.results || [];

        // Add mock data if none exists
        if (allBlogPosts.length === 0) {
            allBlogPosts = getMockBlogPosts();
        }

        // Clear loading skeleton
        blogPostsList.innerHTML = '';

        if (allBlogPosts.length === 0) {
            blogPostsList.innerHTML = '<p class="loading">No blog posts available yet.</p>';
            return;
        }

        renderBlogPosts(allBlogPosts);
    } catch (error) {
        console.error('Error fetching blog posts:', error);
        // Use mock data on error
        allBlogPosts = getMockBlogPosts();
        renderBlogPosts(allBlogPosts);
    } finally {
        isLoadingBlogs = false;
    }
}

// Mock blog posts
function getMockBlogPosts(): BlogPost[] {
    return [
        {
            id: 1,
            title: 'Getting Started with TypeScript',
            slug: 'getting-started-typescript',
            content: 'TypeScript has become an essential tool for modern web development. In this comprehensive guide, we\'ll explore the fundamentals of TypeScript and how it can improve your development workflow. From basic types to advanced features like generics and decorators, we\'ll cover everything you need to know to get started with TypeScript in your projects.',
            author: 1,
            author_name: 'John Doe',
            published_date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
            updated_at: new Date().toISOString(),
            category: 'Tutorial',
            read_time: 5
        },
        {
            id: 2,
            title: 'Building RESTful APIs with Django',
            slug: 'building-restful-apis-django',
            content: 'Django REST Framework is a powerful toolkit for building Web APIs. In this article, we\'ll walk through creating a complete RESTful API from scratch. We\'ll cover serializers, viewsets, authentication, permissions, and best practices for API design. By the end, you\'ll have a solid understanding of how to build production-ready APIs with Django.',
            author: 1,
            author_name: 'John Doe',
            published_date: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000).toISOString(),
            updated_at: new Date().toISOString(),
            category: 'Backend',
            read_time: 8
        },
        {
            id: 3,
            title: 'Modern CSS Techniques',
            slug: 'modern-css-techniques',
            content: 'CSS has evolved significantly in recent years. From CSS Grid and Flexbox to custom properties and animations, modern CSS provides powerful tools for creating beautiful, responsive layouts. In this post, we\'ll explore some of the most useful modern CSS techniques and how to apply them in your projects. Learn how to create stunning designs without relying heavily on JavaScript.',
            author: 1,
            author_name: 'John Doe',
            published_date: new Date(Date.now() - 21 * 24 * 60 * 60 * 1000).toISOString(),
            updated_at: new Date().toISOString(),
            category: 'Frontend',
            read_time: 6
        }
    ];
}

// Render blog posts
function renderBlogPosts(posts: BlogPost[]): void {
    const blogPostsList = document.getElementById('blog-posts-list');
    if (!blogPostsList) return;

    blogPostsList.innerHTML = '';

    const filteredPosts = currentBlogCategory === 'all' 
        ? posts 
        : posts.filter(p => p.category === currentBlogCategory);

    if (filteredPosts.length === 0) {
        blogPostsList.innerHTML = '<p class="loading">No blog posts found.</p>';
        return;
    }

    filteredPosts.forEach(post => {
        const blogCard = createBlogCard(post);
        blogPostsList.appendChild(blogCard);
    });
}

// Create a blog card element
function createBlogCard(post: BlogPost): HTMLElement {
    const card = document.createElement('div');
    card.className = 'blog-card animate-on-scroll';

    // Title
    const title = document.createElement('h3');
    title.textContent = post.title;
    card.appendChild(title);

    // Meta information
    const meta = document.createElement('div');
    meta.className = 'blog-meta';
    
    const readTime = post.read_time || calculateReadTime(post.content);
    meta.innerHTML = `
        <span><i class="fas fa-user"></i> ${post.author_name}</span>
        <span><i class="fas fa-calendar"></i> ${formatDate(post.published_date)}</span>
        <span class="read-time"><i class="fas fa-clock"></i> ${readTime} min read</span>
    `;
    card.appendChild(meta);

    // Excerpt
    const excerpt = document.createElement('p');
    excerpt.className = 'blog-excerpt';
    const maxLength = 150;
    const truncatedContent = post.content.length > maxLength
        ? post.content.substring(0, maxLength) + '...'
        : post.content;
    excerpt.textContent = truncatedContent;
    card.appendChild(excerpt);

    // Category tag
    if (post.category) {
        const tagsContainer = document.createElement('div');
        tagsContainer.className = 'blog-tags';
        const tag = document.createElement('span');
        tag.className = 'blog-tag';
        tag.textContent = post.category;
        tagsContainer.appendChild(tag);
        card.appendChild(tagsContainer);
    }

    // Read more link
    const readMore = document.createElement('a');
    readMore.href = `#blog-${post.slug}`;
    readMore.className = 'read-more';
    readMore.innerHTML = 'Read More <i class="fas fa-arrow-right"></i>';
    card.appendChild(readMore);

    // Share buttons
    const shareButtons = document.createElement('div');
    shareButtons.className = 'share-buttons';
    shareButtons.innerHTML = `
        <button class="share-btn twitter" aria-label="Share on Twitter">
            <i class="fab fa-twitter"></i>
        </button>
        <button class="share-btn facebook" aria-label="Share on Facebook">
            <i class="fab fa-facebook"></i>
        </button>
        <button class="share-btn linkedin" aria-label="Share on LinkedIn">
            <i class="fab fa-linkedin"></i>
        </button>
    `;
    card.appendChild(shareButtons);

    // Add share functionality
    const shareUrl = window.location.origin + `#blog-${post.slug}`;
    const shareTitle = post.title;

    shareButtons.querySelector('.twitter')?.addEventListener('click', () => {
        window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(shareUrl)}&text=${encodeURIComponent(shareTitle)}`, '_blank');
    });

    shareButtons.querySelector('.facebook')?.addEventListener('click', () => {
        window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`, '_blank');
    });

    shareButtons.querySelector('.linkedin')?.addEventListener('click', () => {
        window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareUrl)}`, '_blank');
    });

    return card;
}

// Blog search functionality
function setupBlogSearch(): void {
    const searchInput = document.getElementById('blog-search') as HTMLInputElement;
    if (!searchInput) return;

    const handleSearch = debounce((searchTerm: string) => {
        const filtered = allBlogPosts.filter(post => 
            post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
            post.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
            (post.category && post.category.toLowerCase().includes(searchTerm.toLowerCase()))
        );
        renderBlogPosts(filtered);
        setupScrollAnimations();
    }, 300);

    searchInput.addEventListener('input', (e) => {
        const target = e.target as HTMLInputElement;
        handleSearch(target.value);
    });
}

// Blog category filtering
function setupBlogCategories(): void {
    const categoriesContainer = document.getElementById('blog-categories');
    if (!categoriesContainer) return;

    // Extract unique categories
    const categories = ['all', ...new Set(allBlogPosts.map(p => p.category).filter(Boolean))];

    categories.forEach(category => {
        const button = document.createElement('button');
        button.className = `category-tag${category === 'all' ? ' active' : ''}`;
        button.setAttribute('data-category', category || 'all');
        button.textContent = category === 'all' ? 'All' : category as string;
        
        button.addEventListener('click', () => {
            document.querySelectorAll('.category-tag').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            currentBlogCategory = category || 'all';
            renderBlogPosts(allBlogPosts);
            setupScrollAnimations();
        });
        
        categoriesContainer.appendChild(button);
    });
}

// Form validation
function validateEmail(email: string): boolean {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateField(field: HTMLInputElement | HTMLTextAreaElement, errorElement: HTMLElement): boolean {
    const value = field.value.trim();
    
    if (!value && field.required) {
        errorElement.textContent = 'This field is required';
        field.classList.add('error');
        field.classList.remove('success');
        return false;
    }
    
    if (field.type === 'email' && !validateEmail(value)) {
        errorElement.textContent = 'Please enter a valid email address';
        field.classList.add('error');
        field.classList.remove('success');
        return false;
    }
    
    if (field.name === 'message' && value.length < 10) {
        errorElement.textContent = 'Message must be at least 10 characters';
        field.classList.add('error');
        field.classList.remove('success');
        return false;
    }
    
    errorElement.textContent = '';
    field.classList.remove('error');
    field.classList.add('success');
    return true;
}

// Real-time validation
function setupFormValidation(): void {
    const form = document.getElementById('contact-form') as HTMLFormElement;
    if (!form) return;

    const nameInput = document.getElementById('name') as HTMLInputElement;
    const emailInput = document.getElementById('email') as HTMLInputElement;
    const messageTextarea = document.getElementById('message') as HTMLTextAreaElement;

    const nameError = document.getElementById('name-error') as HTMLElement;
    const emailError = document.getElementById('email-error') as HTMLElement;
    const messageError = document.getElementById('message-error') as HTMLElement;

    if (!nameInput || !emailInput || !messageTextarea || !nameError || !emailError || !messageError) return;

    // Real-time validation on blur
    nameInput.addEventListener('blur', () => validateField(nameInput, nameError));
    emailInput.addEventListener('blur', () => validateField(emailInput, emailError));
    messageTextarea.addEventListener('blur', () => validateField(messageTextarea, messageError));

    // Clear error on input
    [nameInput, emailInput, messageTextarea].forEach(field => {
        field.addEventListener('input', () => {
            if (field.classList.contains('error')) {
                const errorId = `${field.id}-error`;
                const errorElement = document.getElementById(errorId);
                if (errorElement) {
                    errorElement.textContent = '';
                }
                field.classList.remove('error');
            }
        });
    });
}

// Handle contact form submission
async function handleContactForm(event: Event): Promise<void> {
    event.preventDefault();

    const form = event.target as HTMLFormElement;
    const formMessage = document.getElementById('form-message');
    const submitBtn = form.querySelector('.btn-submit') as HTMLButtonElement;
    
    if (!formMessage || !submitBtn) return;

    // Validate all fields
    const nameInput = document.getElementById('name') as HTMLInputElement;
    const emailInput = document.getElementById('email') as HTMLInputElement;
    const messageTextarea = document.getElementById('message') as HTMLTextAreaElement;

    const nameError = document.getElementById('name-error') as HTMLElement;
    const emailError = document.getElementById('email-error') as HTMLElement;
    const messageError = document.getElementById('message-error') as HTMLElement;

    const isNameValid = validateField(nameInput, nameError);
    const isEmailValid = validateField(emailInput, emailError);
    const isMessageValid = validateField(messageTextarea, messageError);

    if (!isNameValid || !isEmailValid || !isMessageValid) {
        return;
    }

    // Get form data
    const formData: ContactFormData = {
        name: nameInput.value.trim(),
        email: emailInput.value.trim(),
        message: messageTextarea.value.trim(),
        subject: (document.getElementById('subject') as HTMLInputElement)?.value.trim() || ''
    };

    // Show loading state
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/contact/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            // Success
            formMessage.textContent = data.message || 'Thank you for your message! I\'ll get back to you soon.';
            formMessage.className = 'form-message success';
            form.reset();
            
            // Clear validation classes
            [nameInput, emailInput, messageTextarea].forEach(field => {
                field.classList.remove('success', 'error');
            });
            
            // Success animation
            confettiAnimation();
        } else {
            // Error
            const errorMessage = data.message || 'Failed to send message. Please try again.';
            formMessage.textContent = errorMessage;
            formMessage.className = 'form-message error';
        }
    } catch (error) {
        console.error('Error submitting form:', error);
        formMessage.textContent = 'Network error. Please check your connection and try again.';
        formMessage.className = 'form-message error';
    } finally {
        // Remove loading state
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;

        // Hide message after 5 seconds
        setTimeout(() => {
            formMessage.style.display = 'none';
        }, 5000);
    }
}

// Simple confetti animation on form success
function confettiAnimation(): void {
    const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe'];
    const confettiCount = 50;

    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.style.position = 'fixed';
        confetti.style.width = '10px';
        confetti.style.height = '10px';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.left = '50%';
        confetti.style.top = '50%';
        confetti.style.borderRadius = '50%';
        confetti.style.pointerEvents = 'none';
        confetti.style.zIndex = '9999';
        document.body.appendChild(confetti);

        const angle = Math.random() * Math.PI * 2;
        const velocity = 5 + Math.random() * 5;
        const vx = Math.cos(angle) * velocity;
        const vy = Math.sin(angle) * velocity;

        let x = window.innerWidth / 2;
        let y = window.innerHeight / 2;
        let opacity = 1;

        function animate() {
            x += vx;
            y += vy + 2; // gravity
            opacity -= 0.02;

            confetti.style.left = x + 'px';
            confetti.style.top = y + 'px';
            confetti.style.opacity = opacity.toString();

            if (opacity > 0) {
                requestAnimationFrame(animate);
            } else {
                confetti.remove();
            }
        }

        animate();
    }
}

// Download CV functionality
function setupDownloadCV(): void {
    const downloadBtn = document.getElementById('download-cv');
    if (!downloadBtn) return;

    downloadBtn.addEventListener('click', (e) => {
        e.preventDefault();
        // Replace with actual CV file path
        const cvUrl = '/path/to/your/cv.pdf';
        const link = document.createElement('a');
        link.href = cvUrl;
        link.download = 'Your_Name_CV.pdf';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
}

// Initialize the application
function init(): void {
    console.log('🚀 Portfolio initializing...');

    // Setup UI features
    setupScrollAnimations();
    setupNavbarScroll();
    setupActiveSection();
    setupMobileMenu();
    setupDarkMode();
    setupBackToTop();
    setupTypingEffect();
    setupCounters();
    setupProjectModal();
    setupFormValidation();
    setupDownloadCV();

    // Fetch and display data
    fetchProjects().then(() => {
        setupProjectFilters();
        setupScrollAnimations(); // Re-setup for new elements
    });

    fetchBlogPosts().then(() => {
        setupBlogCategories();
        setupBlogSearch();
        setupScrollAnimations(); // Re-setup for new elements
    });

    // Add event listener to contact form
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactForm);
    }

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e: Event) => {
            const target = e.target as HTMLAnchorElement;
            const href = target.getAttribute('href');
            
            if (href && href !== '#') {
                e.preventDefault();
                const element = document.querySelector(href);
                if (element) {
                    element.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Progress bar on scroll
    window.addEventListener('scroll', () => {
        updateProgressBar();
    });

    // Initial progress bar update
    updateProgressBar();

    console.log('✨ Portfolio initialized successfully!');
}

// Run initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Keyboard shortcuts (Easter egg)
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to toggle dark mode
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('theme-toggle')?.click();
    }
    
    // Ctrl/Cmd + / to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        const searchInput = document.getElementById('blog-search') as HTMLInputElement;
        searchInput?.focus();
    }
});

// Export for use in other modules if needed
export {
    fetchProjects,
    fetchBlogPosts,
    handleContactForm,
    type Project,
    type BlogPost,
    type ContactFormData
};