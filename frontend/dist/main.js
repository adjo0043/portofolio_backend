"use strict";
const CV = {
    name: 'Djousse Tedongmene Alex',
    heroTitle: 'Futur Actuaire & Data Scientist',
    location: '7011 Ghlin, Belgique',
    email: 'alextedongmene@gmail.com',
    github: 'https://github.com/aldjoted',
    profile: "Étudiant en Master Sciences Actuarielles (ULB) avec un fort background mathématique (UNamur). Passionné par la modélisation stochastique et l'ingénierie logicielle appliquée à la finance. Rigueur théorique et compétences pratiques en C++ et Python.",
    skills: [
        {
            title: 'Mathématiques & Finance',
            items: [
                'Modélisation Stochastique (MCMC)',
                'Optimisation',
                'Théorie du Risque',
                'Analyse Spectrale (Koopman)'
            ]
        },
        {
            title: 'Développement',
            items: ['C++ (OOP)', 'Python (Numpy, Pandas, Sklearn)', 'Julia', 'MATLAB']
        },
        {
            title: 'Outils',
            items: ['Git', 'Linux', 'LaTeX']
        }
    ],
    projects: [
        {
            title: 'Framework C++ Modélisation Épidémique (SEPAIHRD)',
            technologies: ['C++', 'OOP', 'MCMC', 'Optimisation mémoire'],
            bullets: [
                "Conception d'une architecture Orientée Objet (Factory Pattern) pour simuler des dynamiques stochastiques.",
                'Implémentation d’algorithmes de calibration : MCMC (Metropolis-Hastings) et Particle Swarm Optimization (PSO).',
                'Optimisation de la gestion mémoire pour des simulations Monte-Carlo.'
            ],
            codeUrl: 'https://github.com/aldjoted/Mathematical-Modeling-Of-Infectious-Diseases-V1'
        },
        {
            title: 'Analyse Data-Driven (Koopman/EDMD)',
            technologies: ['MATLAB', 'Koopman', 'EDMD', 'Marchés financiers'],
            bullets: [
                "Application de la théorie de l'opérateur de Koopman pour étudier la dynamique des marchés financiers.",
                'Utilisation de l’algorithme EDMD pour identifier des structures cohérentes ("Eigen-portfolios").',
                'Comparaison des approches linéaires (DMD) et non-linéaires pour l’analyse de séries temporelles.'
            ],
            codeUrl: 'https://www.dropbox.com/scl/fo/gk7u4tg2eicwpmgedfep4/AN7WRkEu9yee6olaEJCt6GU?rlkey=qwvapkfz5ofc54ayqxdmrt2h3&st=aq9c3ffi&dl=0'
        },
        {
            title: 'Solvers Itératifs (GMRES)',
            technologies: ['Julia', 'Python', 'GMRES', 'Algèbre linéaire numérique'],
            bullets: [
                "Implémentation de l'algorithme GMRES pour la résolution de systèmes linéaires de grande dimension.",
                'Étude de l’impact du préconditionnement (ILU) sur la vitesse de convergence.',
                'Analyse de la stabilité numérique comparativement aux méthodes directes.'
            ],
            codeUrl: 'https://github.com/aldjoted/GMRES'
        },
        {
            title: "Optimisation d'Horaires (Algorithmes Génétiques)",
            technologies: ['Python', 'Algorithmes génétiques', 'Optimisation'],
            bullets: [
                "Développement d'un algorithme pour la génération d'horaires sous contraintes multiples.",
                'Mise en œuvre d’opérateurs génétiques (sélection, croisement, mutation) et test de paramètres.'
            ],
            codeUrl: 'https://github.com/aldjoted/GeneticAgorithms'
        }
    ],
    education: [
        {
            date: 'Depuis 2025',
            title: 'Master en Sciences Actuarielles',
            subtitle: 'Université Libre de Bruxelles (ULB)'
        },
        {
            date: '2021–2025',
            title: 'Bachelier en Sciences Mathématiques',
            subtitle: 'Université de Namur (UNamur)'
        }
    ]
};
// Intersection Observer for scroll animations
function setupScrollAnimations() {
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
// Navbar scroll effect
function setupNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar)
        return;
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const currentScroll = window.scrollY;
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        }
        else {
            navbar.classList.remove('scrolled');
        }
        lastScroll = currentScroll;
    });
}
// Active section highlighting
function setupActiveSection() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
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
function setupMobileMenu() {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    if (!hamburger || !navMenu)
        return;
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
        const target = e.target;
        if (!hamburger.contains(target) && !navMenu.contains(target)) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}
// Dark mode toggle
function setupDarkMode() {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle)
        return;
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
function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle)
        return;
    const icon = themeToggle.querySelector('i');
    if (!icon)
        return;
    icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
}
function el(tag, className) {
    const node = document.createElement(tag);
    if (className)
        node.className = className;
    return node;
}
function renderSkills() {
    const grid = document.getElementById('skills-grid');
    if (!grid)
        return;
    grid.innerHTML = '';
    for (const group of CV.skills) {
        const card = el('article', 'skill-card animate-on-scroll');
        const title = el('h3');
        title.textContent = group.title;
        card.appendChild(title);
        const list = el('ul', 'skill-items');
        for (const item of group.items) {
            const li = el('li');
            li.textContent = item;
            list.appendChild(li);
        }
        card.appendChild(list);
        grid.appendChild(card);
    }
}
function renderProjects() {
    const list = document.getElementById('projects-list');
    if (!list)
        return;
    list.innerHTML = '';
    for (const project of CV.projects) {
        const card = el('article', 'project-card animate-on-scroll');
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
        const bullets = el('ul', 'project-bullets');
        for (const line of project.bullets) {
            const li = el('li');
            li.textContent = line;
            bullets.appendChild(li);
        }
        card.appendChild(bullets);
        const actions = el('div', 'project-actions');
        const link = el('a', 'btn btn-outline');
        link.href = project.codeUrl || '#';
        link.target = project.codeUrl ? '_blank' : '';
        link.rel = project.codeUrl ? 'noopener noreferrer' : '';
        link.innerHTML = '<i class="fas fa-link" aria-hidden="true"></i><span>Voir le code</span>';
        actions.appendChild(link);
        card.appendChild(actions);
        list.appendChild(card);
    }
}
function renderEducation() {
    const timeline = document.getElementById('education-timeline');
    if (!timeline)
        return;
    timeline.innerHTML = '';
    for (const item of CV.education) {
        const row = el('div', 'timeline-item');
        const date = el('div', 'timeline-date');
        date.textContent = item.date;
        row.appendChild(date);
        const title = el('div', 'timeline-title');
        title.textContent = item.title;
        row.appendChild(title);
        const subtitle = el('p', 'timeline-subtitle');
        subtitle.textContent = item.subtitle;
        row.appendChild(subtitle);
        timeline.appendChild(row);
    }
}
// Initialize the application
function init() {
    // Setup UI features
    setupScrollAnimations();
    setupNavbarScroll();
    setupActiveSection();
    setupMobileMenu();
    setupDarkMode();
    // Render CV-driven sections
    renderSkills();
    renderProjects();
    renderEducation();
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const target = e.target;
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
    setupScrollAnimations();
}
// Run initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
}
else {
    init();
}
// Keyboard shortcut: Ctrl/Cmd + K => thème
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        document.getElementById('theme-toggle')?.click();
    }
});
