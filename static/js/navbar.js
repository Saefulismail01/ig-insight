// Navigation Bar Controller - Left/Right Layout Version
class NavigationBar {
    constructor() {
        this.navbar = document.getElementById('analysisNavbar');
        this.trigger = document.getElementById('navbarDropdownTrigger');
        this.dropdown = document.getElementById('navbarDropdown');
        this.dateRange = document.getElementById('navbarDateRange');
        this.dropdownItems = document.querySelectorAll('.dropdown-item');
        this.isOpen = false;
        this.activeSection = null;

        this.init();
    }

    init() {
        if (!this.trigger || !this.dropdown) {
            console.warn('Navigation bar elements not found');
            return;
        }

        this.setupDropdownToggle();
        this.setupItemClicks();
        this.setupOutsideClick();
        this.setupScrollSpy();
        this.setupEscapeKey();
    }

    setupDropdownToggle() {
        this.trigger.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggle();
        });
    }

    setupItemClicks() {
        this.dropdownItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = item.getAttribute('href');
                const targetSection = document.querySelector(targetId);

                if (targetSection) {
                    this.scrollToSection(targetSection);
                    this.setActiveItem(item);
                    this.close();
                }
            });
        });
    }

    setupOutsideClick() {
        document.addEventListener('click', (e) => {
            if (this.isOpen &&
                !this.dropdown.contains(e.target) &&
                !this.trigger.contains(e.target)) {
                this.close();
            }
        });

        // Also close on scroll
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            if (this.isOpen) {
                clearTimeout(scrollTimeout);
                scrollTimeout = setTimeout(() => {
                    this.close();
                }, 100);
            }
        }, { passive: true });
    }

    setupEscapeKey() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
                this.trigger.focus();
            }
        });
    }

    setupScrollSpy() {
        const sections = document.querySelectorAll('[id]');
        const options = {
            root: null,
            rootMargin: '-15% 0px -75% 0px',
            threshold: 0
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const sectionId = entry.target.id;
                    this.updateActiveFromSection(sectionId);
                }
            });
        }, options);

        // Observe key sections
        const sectionIds = [
            'kpiGrid',
            'engagementCharts',
            'contentTypeAnalysis',
            'outlierAnalysis',
            'qualityAnalysis',
            'captionAnalysis',
            'durationAnalysis'
        ];

        sectionIds.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                observer.observe(el);
            }
        });
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        this.isOpen = true;
        this.dropdown.classList.add('show');
        this.trigger.classList.add('active');
        this.trigger.setAttribute('aria-expanded', 'true');

        // Trap focus within dropdown
        this.trapFocus();
    }

    close() {
        this.isOpen = false;
        this.dropdown.classList.remove('show');
        this.trigger.classList.remove('active');
        this.trigger.setAttribute('aria-expanded', 'false');
    }

    trapFocus() {
        if (!this.isOpen) return;

        const focusableElements = this.dropdown.querySelectorAll('a, button, [tabindex]:not([tabindex="-1"])');
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (firstElement) {
            firstElement.focus();
        }

        const handleTabKey = (e) => {
            if (e.key !== 'Tab') return;

            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                }
            } else {
                if (document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        };

        this.dropdown.addEventListener('keydown', handleTabKey);
    }

    scrollToSection(targetSection) {
        const navbarHeight = this.navbar?.offsetHeight || 80;
        const offset = navbarHeight + 20;
        const elementPosition = targetSection.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }

    setActiveItem(activeItem) {
        this.dropdownItems.forEach(item => item.classList.remove('active'));
        activeItem.classList.add('active');
        this.activeSection = activeItem.dataset.section;
    }

    updateActiveFromSection(sectionId) {
        const correspondingItem = document.querySelector(`.dropdown-item[href="#${sectionId}"]`);

        if (correspondingItem && correspondingItem.dataset.section !== this.activeSection) {
            this.setActiveItem(correspondingItem);
        }
    }

    /**
     * Update date range display
     * @param {string} startDate - Start date string (e.g., "1 Jan 2024")
     * @param {string} endDate - End date string (e.g., "31 Jan 2024")
     */
    setDateRange(startDate, endDate) {
        if (!this.dateRange) return;

        if (startDate && endDate) {
            this.dateRange.textContent = `Date Range: ${startDate} – ${endDate}`;
        } else {
            this.dateRange.textContent = 'Date Range: All Data';
        }
    }

    showNavbar() {
        if (this.navbar) {
            this.navbar.classList.remove('hidden');
            // Smooth fade-in
            this.navbar.style.opacity = '0';
            this.navbar.style.transform = 'translateY(-10px)';
            requestAnimationFrame(() => {
                this.navbar.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                this.navbar.style.opacity = '1';
                this.navbar.style.transform = 'translateY(0)';
            });
        }
    }

    hideNavbar() {
        if (this.navbar) {
            this.navbar.classList.add('hidden');
            this.close();
        }
    }

    destroy() {
        // Cleanup event listeners if needed
        this.close();
    }
}

// Initialize navigation bar
let navBar;

function initializeNavBar() {
    if (!navBar) {
        navBar = new NavigationBar();
        window.navBar = navBar;
        console.log('✅ Navigation Bar initialized (v4.3 - Clean Layout)');
    }
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeNavBar);
} else {
    initializeNavBar();
}

// Listen for data upload to show navbar and set date range
document.addEventListener('dataUploaded', (e) => {
    if (navBar) {
        navBar.showNavbar();

        // Try to extract and format date range from uploaded data
        if (e.detail && e.detail.dateRange) {
            const { start, end } = e.detail.dateRange;
            navBar.setDateRange(start, end);
        } else if (e.detail && e.detail.data) {
            // Try to extract dates from data if not provided
            try {
                const dates = extractDateRange(e.detail.data);
                if (dates) {
                    navBar.setDateRange(dates.start, dates.end);
                }
            } catch (err) {
                console.warn('Could not extract date range:', err);
            }
        }
    }
});

/**
 * Helper function to extract date range from data
 * @param {Array} data - Array of data objects
 * @returns {Object|null} - Object with start and end dates or null
 */
function extractDateRange(data) {
    if (!Array.isArray(data) || data.length === 0) return null;

    try {
        // Find date field (common names)
        const dateFields = ['date', 'posted_at', 'created_at', 'timestamp', 'Date', 'Posted At'];
        let dateField = null;

        for (const field of dateFields) {
            if (data[0].hasOwnProperty(field)) {
                dateField = field;
                break;
            }
        }

        if (!dateField) return null;

        // Get all dates
        const dates = data
            .map(item => new Date(item[dateField]))
            .filter(date => !isNaN(date.getTime()))
            .sort((a, b) => a - b);

        if (dates.length === 0) return null;

        const startDate = dates[0];
        const endDate = dates[dates.length - 1];

        // Format dates
        const formatDate = (date) => {
            const day = date.getDate();
            const month = date.toLocaleString('en', { month: 'short' });
            const year = date.getFullYear();
            return `${day} ${month} ${year}`;
        };

        return {
            start: formatDate(startDate),
            end: formatDate(endDate)
        };
    } catch (err) {
        console.error('Error extracting date range:', err);
        return null;
    }
}

// Export for use in other modules
window.NavigationBar = NavigationBar;
