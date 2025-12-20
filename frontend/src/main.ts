// =============================================================================
// Types - API Response Types
// =============================================================================

interface SocialLink {
    id: number;
    platform: string;
    url: string;
    icon: string;
    icon_class: string;
    order: number;
}

interface Profile {
    id: number;
    full_name: string;
    title: string;
    subtitle: string;
    bio: string;
    short_bio: string;
    email: string;
    phone: string;
    location: string;
    avatar: string | null;
    resume: string | null;
    is_available_for_hire: boolean;
    social_links: SocialLink[];
}

interface SkillItem {
    id: number;
    name: string;
    proficiency: number;
    order: number;
}

interface SkillGroup {
    id: number;
    name: string;
    icon: string;
    order: number;
    items: SkillItem[];
}

interface ExperienceBullet {
    id: number;
    text: string;
    order: number;
}

interface Experience {
    id: number;
    company: string;
    position: string;
    location: string;
    start_date: string;
    end_date: string | null;
    is_current: boolean;
    description: string;
    company_url: string;
    company_logo: string | null;
    bullets: ExperienceBullet[];
}

interface Education {
    id: number;
    institution: string;
    degree: string;
    field_of_study: string;
    start_date: string;
    end_date: string | null;
    is_current: boolean;
    description: string;
    gpa: string;
    institution_logo: string | null;
}

interface Certification {
    id: number;
    name: string;
    issuing_organization: string;
    issue_date: string;
    expiry_date: string | null;
    credential_id: string;
    credential_url: string;
}

interface Language {
    id: number;
    name: string;
    proficiency: string;
    order: number;
}

interface Interest {
    id: number;
    name: string;
    icon: string;
    order: number;
}

interface CustomSectionItem {
    id: number;
    title: string;
    subtitle: string;
    description: string;
    date: string;
    url: string;
    icon: string;
    order: number;
}

interface CustomSection {
    id: number;
    title: string;
    slug: string;
    icon: string;
    order: number;
    show_in_nav: boolean;
    items: CustomSectionItem[];
}

interface ProjectBullet {
    id: number;
    text: string;
    order: number;
}

interface Project {
    id: number;
    title: string;
    slug: string;
    description: string;
    short_description: string;
    featured_image: string | null;
    technologies: string[];
    live_url: string;
    github_url: string;
    is_featured: boolean;
    is_published: boolean;
    order: number;
    bullets: ProjectBullet[];
}

interface PortfolioData {
    profile: Profile | null;
    skills: SkillGroup[];
    experiences: Experience[];
    education: Education[];
    certifications: Certification[];
    languages: Language[];
    interests: Interest[];
    custom_sections: CustomSection[];
    projects: Project[];
}

// =============================================================================
// Configuration
// =============================================================================

const API_BASE_URL = 'http://localhost:8000/api';

// Fallback data in case API is unavailable
const FALLBACK_DATA: PortfolioData = {
    profile: {
        id: 1,
        full_name: 'Djousse Tedongmene Alex',
        title: 'Étudiant Master Actuariat & Finance Quantitative',
        subtitle: 'Futur Actuaire & Data Scientist',
        bio: "Étudiant en Master Sciences Actuarielles (ULB) avec un fort background mathématique (UNamur). Passionné par la modélisation stochastique et l'ingénierie logicielle appliquée à la finance. Rigueur théorique et compétences pratiques en C++ et Python.",
        short_bio: "Étudiant en Master Sciences Actuarielles (ULB) avec un fort background mathématique.",
        email: 'alextedongmene@gmail.com',
        phone: '',
        location: '7011 Ghlin, Belgique',
        avatar: null,
        resume: null,
        is_available_for_hire: true,
        social_links: [
            { id: 1, platform: 'GitHub', url: 'https://github.com/aldjoted', icon: 'github', icon_class: 'fab fa-github', order: 1 }
        ]
    },
    skills: [
        {
            id: 1,
            name: 'Mathématiques & Finance',
            icon: 'fas fa-chart-line',
            order: 1,
            items: [
                { id: 1, name: 'Modélisation Stochastique (MCMC)', proficiency: 90, order: 1 },
                { id: 2, name: 'Optimisation', proficiency: 85, order: 2 },
                { id: 3, name: 'Théorie du Risque', proficiency: 80, order: 3 },
                { id: 4, name: 'Analyse Spectrale (Koopman)', proficiency: 75, order: 4 }
            ]
        },
        {
            id: 2,
            name: 'Développement',
            icon: 'fas fa-code',
            order: 2,
            items: [
                { id: 5, name: 'C++ (OOP)', proficiency: 85, order: 1 },
                { id: 6, name: 'Python (Numpy, Pandas, Sklearn)', proficiency: 90, order: 2 },
                { id: 7, name: 'Julia', proficiency: 70, order: 3 },
                { id: 8, name: 'MATLAB', proficiency: 75, order: 4 }
            ]
        },
        {
            id: 3,
            name: 'Outils',
            icon: 'fas fa-tools',
            order: 3,
            items: [
                { id: 9, name: 'Git', proficiency: 85, order: 1 },
                { id: 10, name: 'Linux', proficiency: 80, order: 2 },
                { id: 11, name: 'LaTeX', proficiency: 90, order: 3 }
            ]
        }
    ],
    experiences: [],
    education: [
        {
            id: 1,
            institution: 'Université Libre de Bruxelles (ULB)',
            degree: 'Master en Sciences Actuarielles',
            field_of_study: 'Sciences Actuarielles',
            start_date: '2025-01-01',
            end_date: null,
            is_current: true,
            description: '',
            gpa: '',
            institution_logo: null
        },
        {
            id: 2,
            institution: 'Université de Namur (UNamur)',
            degree: 'Bachelier en Sciences Mathématiques',
            field_of_study: 'Sciences Mathématiques',
            start_date: '2021-01-01',
            end_date: '2025-01-01',
            is_current: false,
            description: '',
            gpa: '',
            institution_logo: null
        }
    ],
    certifications: [],
    languages: [],
    interests: [],
    custom_sections: [],
    projects: [
        {
            id: 1,
            title: 'Framework C++ Modélisation Épidémique (SEPAIHRD)',
            slug: 'sepaihrd',
            description: '',
            short_description: '',
            featured_image: null,
            technologies: ['C++', 'OOP', 'MCMC', 'Optimisation mémoire'],
            live_url: '',
            github_url: 'https://github.com/aldjoted/Mathematical-Modeling-Of-Infectious-Diseases-V1',
            is_featured: true,
            is_published: true,
            order: 1,
            bullets: [
                { id: 1, text: "Conception d'une architecture Orientée Objet (Factory Pattern) pour simuler des dynamiques stochastiques.", order: 1 },
                { id: 2, text: "Implémentation d'algorithmes de calibration : MCMC (Metropolis-Hastings) et Particle Swarm Optimization (PSO).", order: 2 },
                { id: 3, text: "Optimisation de la gestion mémoire pour des simulations Monte-Carlo.", order: 3 }
            ]
        },
        {
            id: 2,
            title: 'Analyse Data-Driven (Koopman/EDMD)',
            slug: 'koopman-edmd',
            description: '',
            short_description: '',
            featured_image: null,
            technologies: ['MATLAB', 'Koopman', 'EDMD', 'Marchés financiers'],
            live_url: '',
            github_url: 'https://www.dropbox.com/scl/fo/gk7u4tg2eicwpmgedfep4/AN7WRkEu9yee6olaEJCt6GU?rlkey=qwvapkfz5ofc54ayqxdmrt2h3&st=aq9c3ffi&dl=0',
            is_featured: true,
            is_published: true,
            order: 2,
            bullets: [
                { id: 4, text: "Application de la théorie de l'opérateur de Koopman pour étudier la dynamique des marchés financiers.", order: 1 },
                { id: 5, text: "Utilisation de l'algorithme EDMD pour identifier des structures cohérentes (\"Eigen-portfolios\").", order: 2 },
                { id: 6, text: "Comparaison des approches linéaires (DMD) et non-linéaires pour l'analyse de séries temporelles.", order: 3 }
            ]
        },
        {
            id: 3,
            title: 'Solvers Itératifs (GMRES)',
            slug: 'gmres',
            description: '',
            short_description: '',
            featured_image: null,
            technologies: ['Julia', 'Python', 'GMRES', 'Algèbre linéaire numérique'],
            live_url: '',
            github_url: 'https://github.com/aldjoted/GMRES',
            is_featured: true,
            is_published: true,
            order: 3,
            bullets: [
                { id: 7, text: "Implémentation de l'algorithme GMRES pour la résolution de systèmes linéaires de grande dimension.", order: 1 },
                { id: 8, text: "Étude de l'impact du préconditionnement (ILU) sur la vitesse de convergence.", order: 2 },
                { id: 9, text: "Analyse de la stabilité numérique comparativement aux méthodes directes.", order: 3 }
            ]
        },
        {
            id: 4,
            title: "Optimisation d'Horaires (Algorithmes Génétiques)",
            slug: 'genetic-algorithms',
            description: '',
            short_description: '',
            featured_image: null,
            technologies: ['Python', 'Algorithmes génétiques', 'Optimisation'],
            live_url: '',
            github_url: 'https://github.com/aldjoted/GeneticAgorithms',
            is_featured: true,
            is_published: true,
            order: 4,
            bullets: [
                { id: 10, text: "Développement d'un algorithme pour la génération d'horaires sous contraintes multiples.", order: 1 },
                { id: 11, text: "Mise en œuvre d'opérateurs génétiques (sélection, croisement, mutation) et test de paramètres.", order: 2 }
            ]
        }
    ]
};

// Global portfolio data
let portfolioData: PortfolioData = FALLBACK_DATA;

// =============================================================================
// API Functions
// =============================================================================

async function fetchPortfolioData(): Promise<PortfolioData> {
    try {
        const response = await fetch(`${API_BASE_URL}/portfolio/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Portfolio data loaded from API:', data);
        return data;
    } catch (error) {
        console.warn('Failed to fetch portfolio data from API, using fallback:', error);
        return FALLBACK_DATA;
    }
}

// =============================================================================
// UI Setup Functions
// =============================================================================

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

function setupNavbarScroll(): void {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        const currentScroll = window.scrollY;
        
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

function setupActiveSection(): void {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = (section as HTMLElement).offsetTop;
            
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

function setupMobileMenu(): void {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    
    if (!hamburger || !navMenu) return;

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    });

    const navLinks = navMenu.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    document.addEventListener('click', (e) => {
        const target = e.target as HTMLElement;
        if (!hamburger.contains(target) && !navMenu.contains(target)) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

function setupDarkMode(): void {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

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

function setupSmoothScrolling(): void {
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
}

// =============================================================================
// Helper Functions
// =============================================================================

function el<K extends keyof HTMLElementTagNameMap>(tag: K, className?: string): HTMLElementTagNameMap[K] {
    const node = document.createElement(tag);
    if (className) node.className = className;
    return node;
}

function formatDateRange(startDate: string, endDate: string | null, isCurrent: boolean): string {
    const start = new Date(startDate);
    const startYear = start.getFullYear();
    
    if (isCurrent) {
        return `Depuis ${startYear}`;
    }
    
    if (endDate) {
        const end = new Date(endDate);
        const endYear = end.getFullYear();
        return `${startYear}–${endYear}`;
    }
    
    return `${startYear}`;
}

// =============================================================================
// Render Functions
// =============================================================================

function renderHero(): void {
    const profile = portfolioData.profile;
    if (!profile) return;

    // Update hero content
    const heroTitle = document.querySelector('.hero-title');
    const heroSubtitle = document.querySelector('.hero-subtitle');
    const heroEyebrow = document.querySelector('.hero-eyebrow');
    const heroDescription = document.querySelector('.hero-description');

    if (heroTitle) heroTitle.textContent = profile.full_name;
    if (heroSubtitle) heroSubtitle.textContent = profile.subtitle;
    if (heroEyebrow) heroEyebrow.textContent = profile.title;
    if (heroDescription) heroDescription.textContent = profile.bio;

    // Update hero meta (location, email, social links)
    const heroMeta = document.querySelector('.hero-meta');
    if (heroMeta) {
        heroMeta.innerHTML = '';
        
        // Location
        if (profile.location) {
            const locationLi = el('li');
            locationLi.innerHTML = `<i class="fas fa-location-dot" aria-hidden="true"></i><span>${profile.location}</span>`;
            heroMeta.appendChild(locationLi);
        }
        
        // Email
        if (profile.email) {
            const emailLi = el('li');
            emailLi.innerHTML = `<i class="fas fa-envelope" aria-hidden="true"></i><a href="mailto:${profile.email}">${profile.email}</a>`;
            heroMeta.appendChild(emailLi);
        }
        
        // Social links
        for (const social of profile.social_links) {
            const socialLi = el('li');
            const iconClass = social.icon_class || social.icon || `fab fa-${social.platform.toLowerCase()}`;
            socialLi.innerHTML = `<i class="${iconClass}" aria-hidden="true"></i><a href="${social.url}" target="_blank" rel="noopener noreferrer">${social.url.replace(/^https?:\/\//, '')}</a>`;
            heroMeta.appendChild(socialLi);
        }
    }

    // Update contact button
    const contactBtn = document.querySelector('.hero-cta .btn-secondary') as HTMLAnchorElement;
    if (contactBtn && profile.email) {
        contactBtn.href = `mailto:${profile.email}`;
    }

    // Render Profile Image if available
    const heroContainer = document.querySelector('.hero-container');
    const existingImage = document.querySelector('.hero-image-container');
    
    if (profile.avatar && heroContainer) {
        if (!existingImage) {
            const imageContainer = el('div', 'hero-image-container animate-fade-in');
            const img = el('img', 'hero-avatar') as HTMLImageElement;
            img.src = profile.avatar;
            img.alt = profile.full_name;
            imageContainer.appendChild(img);
            
            // Insert before content if desktop, or adjust via CSS order
            heroContainer.appendChild(imageContainer);
            heroContainer.classList.add('has-image');
        } else {
            const img = existingImage.querySelector('img');
            if (img) img.src = profile.avatar;
        }
    } else if (existingImage) {
        existingImage.remove();
        heroContainer?.classList.remove('has-image');
    }
}

function renderAbout(): void {
    const profile = portfolioData.profile;
    if (!profile) return;

    const aboutContent = document.querySelector('.about-content .lead');
    if (aboutContent) {
        aboutContent.textContent = profile.bio;
    }
}

function renderSkills(): void {
    const grid = document.getElementById('skills-grid');
    if (!grid) return;

    grid.innerHTML = '';

    for (const group of portfolioData.skills) {
        const card = el('article', 'skill-card animate-on-scroll');
        
        const titleContainer = el('div', 'skill-title-container');
        if (group.icon) {
            const icon = el('i');
            icon.className = group.icon;
            titleContainer.appendChild(icon);
        }
        const title = el('h3');
        title.textContent = group.name;
        titleContainer.appendChild(title);
        card.appendChild(titleContainer);

        const list = el('ul', 'skill-items');
        for (const item of group.items) {
            const li = el('li');
            li.textContent = item.name;
            
            // Add proficiency bar if proficiency is set
            if (item.proficiency > 0) {
                const proficiencyBar = el('div', 'proficiency-bar');
                const proficiencyFill = el('div', 'proficiency-fill');
                proficiencyFill.style.width = `${item.proficiency}%`;
                proficiencyBar.appendChild(proficiencyFill);
                li.appendChild(proficiencyBar);
            }
            
            list.appendChild(li);
        }
        card.appendChild(list);

        grid.appendChild(card);
    }
}

function renderProjects(): void {
    const list = document.getElementById('projects-list');
    if (!list) return;

    list.innerHTML = '';

    const publishedProjects = portfolioData.projects.filter(p => p.is_published);

    for (const project of publishedProjects) {
        const card = el('article', 'project-card animate-on-scroll');

        // Featured image
        if (project.featured_image) {
            const imageContainer = el('div', 'project-image');
            const img = el('img') as HTMLImageElement;
            img.src = project.featured_image;
            img.alt = project.title;
            img.loading = 'lazy';
            imageContainer.appendChild(img);
            card.appendChild(imageContainer);
        }

        const header = el('div', 'project-header');

        const h3 = el('h3', 'project-title');
        h3.textContent = project.title;
        header.appendChild(h3);

        const meta = el('div', 'project-meta');
        for (const tech of project.technologies) {
            const chip = el('span', 'chip');
            chip.textContent = tech;
            meta.appendChild(chip);
        }
        header.appendChild(meta);

        card.appendChild(header);

        // Description or bullets
        if (project.bullets && project.bullets.length > 0) {
            const bullets = el('ul', 'project-bullets');
            for (const bullet of project.bullets) {
                const li = el('li');
                li.textContent = bullet.text;
                bullets.appendChild(li);
            }
            card.appendChild(bullets);
        } else if (project.description) {
            const desc = el('p', 'project-description');
            desc.textContent = project.short_description || project.description;
            card.appendChild(desc);
        }

        // Actions
        const actions = el('div', 'project-actions');
        
        if (project.github_url) {
            const codeLink = el('a', 'btn btn-outline') as HTMLAnchorElement;
            codeLink.href = project.github_url;
            codeLink.target = '_blank';
            codeLink.rel = 'noopener noreferrer';
            codeLink.innerHTML = '<i class="fas fa-code" aria-hidden="true"></i><span>Code</span>';
            actions.appendChild(codeLink);
        }
        
        if (project.live_url) {
            const liveLink = el('a', 'btn btn-primary') as HTMLAnchorElement;
            liveLink.href = project.live_url;
            liveLink.target = '_blank';
            liveLink.rel = 'noopener noreferrer';
            liveLink.innerHTML = '<i class="fas fa-external-link-alt" aria-hidden="true"></i><span>Demo</span>';
            actions.appendChild(liveLink);
        }

        if (actions.children.length > 0) {
            card.appendChild(actions);
        }

        list.appendChild(card);
    }
}

function renderEducation(): void {
    const timeline = document.getElementById('education-timeline');
    if (!timeline) return;

    timeline.innerHTML = '';

    for (const item of portfolioData.education) {
        const row = el('div', 'timeline-item');

        const date = el('div', 'timeline-date');
        date.textContent = formatDateRange(item.start_date, item.end_date, item.is_current);
        row.appendChild(date);

        const content = el('div', 'timeline-content');
        
        const title = el('div', 'timeline-title');
        title.textContent = item.degree;
        content.appendChild(title);

        const subtitle = el('p', 'timeline-subtitle');
        subtitle.textContent = item.institution;
        content.appendChild(subtitle);

        if (item.field_of_study && item.field_of_study !== item.degree) {
            const field = el('p', 'timeline-field');
            field.textContent = item.field_of_study;
            content.appendChild(field);
        }

        if (item.description) {
            const desc = el('p', 'timeline-description');
            desc.textContent = item.description;
            content.appendChild(desc);
        }

        row.appendChild(content);
        timeline.appendChild(row);
    }
}

function renderExperiences(): void {
    const container = document.getElementById('experiences-container');
    if (!container || portfolioData.experiences.length === 0) return;

    // Show the experiences section
    const section = document.getElementById('experiences');
    if (section) section.style.display = 'block';

    container.innerHTML = '';

    for (const exp of portfolioData.experiences) {
        const card = el('article', 'experience-card animate-on-scroll');

        const header = el('div', 'experience-header');
        
        if (exp.company_logo) {
            const logo = el('img', 'company-logo') as HTMLImageElement;
            logo.src = exp.company_logo;
            logo.alt = exp.company;
            header.appendChild(logo);
        }

        const headerContent = el('div', 'experience-header-content');
        
        const position = el('h3', 'experience-position');
        position.textContent = exp.position;
        headerContent.appendChild(position);

        const company = el('div', 'experience-company');
        if (exp.company_url) {
            const companyLink = el('a') as HTMLAnchorElement;
            companyLink.href = exp.company_url;
            companyLink.target = '_blank';
            companyLink.rel = 'noopener noreferrer';
            companyLink.textContent = exp.company;
            company.appendChild(companyLink);
        } else {
            company.textContent = exp.company;
        }
        headerContent.appendChild(company);

        const meta = el('div', 'experience-meta');
        meta.innerHTML = `
            <span><i class="fas fa-calendar" aria-hidden="true"></i>${formatDateRange(exp.start_date, exp.end_date, exp.is_current)}</span>
            ${exp.location ? `<span><i class="fas fa-location-dot" aria-hidden="true"></i>${exp.location}</span>` : ''}
        `;
        headerContent.appendChild(meta);

        header.appendChild(headerContent);
        card.appendChild(header);

        if (exp.description) {
            const desc = el('p', 'experience-description');
            desc.textContent = exp.description;
            card.appendChild(desc);
        }

        if (exp.bullets && exp.bullets.length > 0) {
            const bullets = el('ul', 'experience-bullets');
            for (const bullet of exp.bullets) {
                const li = el('li');
                li.textContent = bullet.text;
                bullets.appendChild(li);
            }
            card.appendChild(bullets);
        }

        container.appendChild(card);
    }
}

function renderCertifications(): void {
    const container = document.getElementById('certifications-container');
    if (!container || portfolioData.certifications.length === 0) return;

    // Show the certifications section
    const section = document.getElementById('certifications');
    if (section) section.style.display = 'block';

    container.innerHTML = '';

    for (const cert of portfolioData.certifications) {
        const card = el('article', 'certification-card animate-on-scroll');

        const title = el('h3', 'certification-title');
        title.textContent = cert.name;
        card.appendChild(title);

        const org = el('div', 'certification-org');
        org.textContent = cert.issuing_organization;
        card.appendChild(org);

        const date = el('div', 'certification-date');
        const issueDate = new Date(cert.issue_date);
        date.textContent = `Délivré: ${issueDate.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })}`;
        if (cert.expiry_date) {
            const expiryDate = new Date(cert.expiry_date);
            date.textContent += ` • Expire: ${expiryDate.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })}`;
        }
        card.appendChild(date);

        if (cert.credential_url) {
            const link = el('a', 'btn btn-outline btn-sm') as HTMLAnchorElement;
            link.href = cert.credential_url;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            link.innerHTML = '<i class="fas fa-external-link-alt" aria-hidden="true"></i><span>Voir le certificat</span>';
            card.appendChild(link);
        }

        container.appendChild(card);
    }
}

function renderLanguages(): void {
    const container = document.getElementById('languages-container');
    if (!container || portfolioData.languages.length === 0) return;

    // Show the languages section
    const section = document.getElementById('languages');
    if (section) section.style.display = 'block';

    container.innerHTML = '';

    for (const lang of portfolioData.languages) {
        const item = el('div', 'language-item');
        
        const name = el('span', 'language-name');
        name.textContent = lang.name;
        item.appendChild(name);

        const proficiency = el('span', 'language-proficiency');
        proficiency.textContent = lang.proficiency;
        item.appendChild(proficiency);

        container.appendChild(item);
    }
}

function renderInterests(): void {
    const container = document.getElementById('interests-container');
    if (!container || portfolioData.interests.length === 0) return;

    // Show the interests section
    const section = document.getElementById('interests');
    if (section) section.style.display = 'block';

    container.innerHTML = '';

    for (const interest of portfolioData.interests) {
        const item = el('div', 'interest-item');
        
        if (interest.icon) {
            const icon = el('i');
            icon.className = interest.icon;
            item.appendChild(icon);
        }

        const name = el('span', 'interest-name');
        name.textContent = interest.name;
        item.appendChild(name);

        container.appendChild(item);
    }
}

function renderCustomSections(): void {
    const customSectionsContainer = document.getElementById('custom-sections-container');
    if (!customSectionsContainer) return;

    customSectionsContainer.innerHTML = '';

    for (const section of portfolioData.custom_sections) {
        if (section.items.length === 0) continue;

        const sectionEl = el('section', 'custom-section');
        sectionEl.id = section.slug;

        const container = el('div', 'container');
        
        // Section header
        const header = el('div', 'section-header animate-on-scroll');
        
        const label = el('span', 'section-label');
        label.textContent = section.title;
        header.appendChild(label);

        const title = el('h2', 'section-title');
        if (section.icon) {
            const icon = el('i');
            icon.className = section.icon;
            title.appendChild(icon);
            title.appendChild(document.createTextNode(' '));
        }
        title.appendChild(document.createTextNode(section.title));
        header.appendChild(title);

        const divider = el('div', 'section-divider');
        header.appendChild(divider);

        container.appendChild(header);

        // Section items
        const itemsContainer = el('div', 'custom-section-items animate-on-scroll');
        
        for (const item of section.items) {
            const card = el('article', 'custom-section-item');

            if (item.icon) {
                const iconEl = el('i', 'custom-item-icon');
                iconEl.className = item.icon;
                card.appendChild(iconEl);
            }

            const content = el('div', 'custom-item-content');

            const itemTitle = el('h3', 'custom-item-title');
            if (item.url) {
                const link = el('a') as HTMLAnchorElement;
                link.href = item.url;
                link.target = '_blank';
                link.rel = 'noopener noreferrer';
                link.textContent = item.title;
                itemTitle.appendChild(link);
            } else {
                itemTitle.textContent = item.title;
            }
            content.appendChild(itemTitle);

            if (item.subtitle) {
                const subtitle = el('div', 'custom-item-subtitle');
                subtitle.textContent = item.subtitle;
                content.appendChild(subtitle);
            }

            if (item.date) {
                const date = el('div', 'custom-item-date');
                date.textContent = item.date;
                content.appendChild(date);
            }

            if (item.description) {
                const desc = el('p', 'custom-item-description');
                desc.textContent = item.description;
                content.appendChild(desc);
            }

            card.appendChild(content);
            itemsContainer.appendChild(card);
        }

        container.appendChild(itemsContainer);
        sectionEl.appendChild(container);
        customSectionsContainer.appendChild(sectionEl);

        // Add to navigation if show_in_nav is true
        if (section.show_in_nav) {
            addCustomSectionToNav(section);
        }
    }
}

function addCustomSectionToNav(section: CustomSection): void {
    const navMenu = document.getElementById('nav-menu');
    if (!navMenu) return;

    // Find the theme toggle button's parent li to insert before it
    const themeToggleLi = navMenu.querySelector('li:last-child');
    
    const li = el('li');
    const link = el('a', 'nav-link') as HTMLAnchorElement;
    link.href = `#${section.slug}`;
    link.setAttribute('data-section', section.slug);
    link.textContent = section.title;
    li.appendChild(link);

    if (themeToggleLi) {
        navMenu.insertBefore(li, themeToggleLi);
    } else {
        navMenu.appendChild(li);
    }
}

function renderFooter(): void {
    const profile = portfolioData.profile;
    if (!profile) return;

    const footerName = document.querySelector('.footer-name');
    const footerTitle = document.querySelector('.footer-title');
    const footerRight = document.querySelector('.footer-right');

    if (footerName) footerName.textContent = profile.full_name;
    if (footerTitle) footerTitle.textContent = profile.title;

    if (footerRight) {
        footerRight.innerHTML = '';

        // Email link
        if (profile.email) {
            const emailLink = el('a', 'footer-link') as HTMLAnchorElement;
            emailLink.href = `mailto:${profile.email}`;
            emailLink.innerHTML = '<i class="fas fa-envelope" aria-hidden="true"></i><span>Email</span>';
            footerRight.appendChild(emailLink);
        }

        // Social links
        for (const social of profile.social_links) {
            const link = el('a', 'footer-link') as HTMLAnchorElement;
            link.href = social.url;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            const iconClass = social.icon_class || social.icon || `fab fa-${social.platform.toLowerCase()}`;
            link.innerHTML = `<i class="${iconClass}" aria-hidden="true"></i><span>${social.platform}</span>`;
            footerRight.appendChild(link);
        }
    }
}

// =============================================================================
// Initialization
// =============================================================================

async function init(): Promise<void> {
    // Fetch portfolio data from API
    portfolioData = await fetchPortfolioData();

    // Setup UI features
    setupScrollAnimations();
    setupNavbarScroll();
    setupActiveSection();
    setupMobileMenu();
    setupDarkMode();
    setupSmoothScrolling();

    // Render all sections
    renderHero();
    renderAbout();
    renderSkills();
    renderProjects();
    renderEducation();
    renderExperiences();
    renderCertifications();
    renderLanguages();
    renderInterests();
    renderCustomSections();
    renderFooter();

    // Re-setup scroll animations for dynamically added elements
    setupScrollAnimations();
}

// Run initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Keyboard shortcut: Ctrl/Cmd + K => thème
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        document.getElementById('theme-toggle')?.click();
    }
});
