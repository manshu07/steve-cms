/**
 * Scroll Reveal Animations
 * IntersectionObserver-based reveal animations for content blocks
 */

(function() {
    'use strict';

    function initScrollReveal() {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    // Optional: stop observing once revealed
                    // observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Elements to animate
        const revealElements = document.querySelectorAll(
            '.cms-prose, .cms-cta, .cms-callout, .cms-feature-grid, .cms-faq, .cms-quote, ' +
            '.cms-comparison, .cms-pricing, .cms-logo-cloud, .cms-gallery-wrap, .cms-table'
        );

        revealElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
            observer.observe(el);
        });

        // Add revealed class styles dynamically
        const style = document.createElement('style');
        style.textContent = `
            .revealed {
                opacity: 1 !important;
                transform: translateY(0) !important;
            }
        `;
        document.head.appendChild(style);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initScrollReveal);
    } else {
        initScrollReveal();
    }
})();
