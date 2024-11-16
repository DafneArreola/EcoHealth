// animations.js

// Scroll-triggered animations
window.addEventListener('scroll', () => {
    const elements = document.querySelectorAll('.scroll-triggered');
    elements.forEach((el) => {
        const position = el.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.5;

        if (position < screenPosition) {
            el.style.opacity = 1;
            el.style.transform = 'translateY(0)';
        }
    });
});

// Animate the hero title and subtitle
document.addEventListener("DOMContentLoaded", () => {
    gsap.from(".hero-title", { duration: 2, opacity: 0, y: -50 });
    gsap.from(".hero-subtitle", { duration: 2, opacity: 0, y: 50, delay: 0.5 });
});

// Example: Animate the call-to-action button
gsap.from(".cta-button", { duration: 2, opacity: 0, scale: 0.8, delay: 1 });

// Additional Animations
// You can add animations for other elements like the animated circles or lines
gsap.to(".animated-circle", {
    duration: 5,
    x: 100,
    y: 50,
    repeat: -1,
    yoyo: true,
    ease: "power1.inOut",
});

gsap.to(".animated-line", {
    duration: 3,
    y: -50,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut",
});
