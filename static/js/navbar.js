// Navigation Bar Controller
class NavigationBar {
    constructor() {
        this.navbar = document.getElementById('analysisNavbar');
        this.navLinks = document.querySelectorAll('.nav-link');
        this.navbarToggle = document.getElementById('navbarToggle');
        this.isMenuOpen = false;
        this.activeSection = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupScrollSpy();
        this.setupMobileMenu();
    }

    setupEventListeners() {
        // Navigation link clicks
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href');
                const targetSection = document.querySelector(targetId);
                
                if (targetSection) {
                    this.scrollToSection(targetSection);
                    this.setActiveLink(link);
                    
                    // Close mobile menu if open
                    if (this.isMenuOpen) {
                        this.toggleMobileMenu();
                    }
                }
            });
        });

        // Show navbar after data is loaded
        document.addEventListener('dataUploaded', () => {
            this.showNavbar();
        });
    }

    setupScrollSpy() {
        const sections = document.querySelectorAll('section[id]');
        const options = {
            root: null,
            rootMargin: '-20% 0px -70% 0px',
            threshold: 0
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const sectionId = entry.target.id;
                    this.updateActiveSection(sectionId);
                }
            });
        }, options);

        sections.forEach(section => observer.observe(section));
    }

    setupMobileMenu() {
        if (this.navbarToggle) {
            this.navbarToggle.addEventListener('click', () => {
                this.toggleMobileMenu();
            });

            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (this.isMenuOpen && 
                    !this.navbar.contains(e.target) && 
                    !this.navbarToggle.contains(e.target)) {
                    this.toggleMobileMenu();
                }
            });
        }
    }

    toggleMobileMenu() {
        this.isMenuOpen = !this.isMenuOpen;
        const navLinks = document.querySelector('.navbar-links');
        
        if (this.isMenuOpen) {
            navLinks.classList.add('active');
            this.navbarToggle.classList.add('active');
            this.navbarToggle.innerHTML = '<span>✕</span>';
            document.body.style.overflow = 'hidden';
        } else {
            navLinks.classList.remove('active');
            this.navbarToggle.classList.remove('active');
            this.navbarToggle.innerHTML = '<span>☰</span>';
            document.body.style.overflow = '';
        }
    }

    scrollToSection(targetSection) {
        const headerOffset = 100; // Account for sticky header
        const elementPosition = targetSection.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }

    setActiveLink(activeLink) {
        this.navLinks.forEach(link => link.classList.remove('active'));
        activeLink.classList.add('active');
        this.activeSection = activeLink.dataset.section;
    }

    updateActiveSection(sectionId) {
        const correspondingLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);
        if (correspondingLink && correspondingLink.dataset.section !== this.activeSection) {
            this.setActiveLink(correspondingLink);
        }
    }

    showNavbar() {
        if (this.navbar) {
            this.navbar.classList.remove('hidden');
            
            // Animate entrance
            setTimeout(() => {
                this.navbar.style.opacity = '1';
                this.navbar.style.transform = 'translateY(0)';
            }, 100);
        }
    }

    hideNavbar() {
        if (this.navbar) {
            this.navbar.style.opacity = '0';
            this.navbar.style.transform = 'translateY(-100%)';
            
            setTimeout(() => {
                this.navbar.classList.add('hidden');
            }, 300);
        }
    }

    // Public method to programmatically navigate to section
    navigateToSection(sectionName) {
        const link = document.querySelector(`.nav-link[data-section="${sectionName}"]`);
        if (link) {
            link.click();
        }
    }

    // Get current active section
    getCurrentSection() {
        return this.activeSection;
    }
}

// Initialize navigation bar
const navBar = new NavigationBar();

// Make it globally accessible
window.navBar = navBar;
