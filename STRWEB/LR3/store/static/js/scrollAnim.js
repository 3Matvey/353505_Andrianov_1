// scrollAnim.js — simple parallax/scroll animation for images
(function(){
  'use strict';

  function clamp(v, a, b){ return Math.max(a, Math.min(b, v)); }

  document.addEventListener('DOMContentLoaded', () => {
    const items = Array.from(document.querySelectorAll('.anim-item'));
    if (!items.length) return;

    // for each item we keep state
    const states = items.map(el => {
      const img = el.querySelector('img');
      const speed = parseFloat(el.dataset.speed) || 0.3;
      return { el, img, speed, lastY: 0 };
    });

    let ticking = false;

    function update() {
      const viewportH = window.innerHeight;
      states.forEach(s => {
        const rect = s.el.getBoundingClientRect();
        // compute how far the element's center is from viewport center (-1..1)
        const elCenter = rect.top + rect.height / 2;
        const norm = (elCenter - viewportH / 2) / (viewportH / 2); // -inf..inf, roughly -1..1 around center
        // compute translation based on speed and normalized position
        // direction: negative norm moves image up when scrolling down if speed>0
        const maxOffset = 30; // px
        const translateY = clamp(-norm * s.speed * maxOffset, -maxOffset, maxOffset);
        // apply transform to image
        if (s.img) {
          s.img.style.transform = `translate(-50%, calc(-50% + ${translateY}px))`;
        }
      });
      ticking = false;
    }

    function requestUpdate(){ if (!ticking){ ticking = true; requestAnimationFrame(update); } }

    // initial update
    requestUpdate();

    // update on scroll and resize
    window.addEventListener('scroll', requestUpdate, { passive: true });
    window.addEventListener('resize', requestUpdate);

    // also update on orientationchange (mobile)
    window.addEventListener('orientationchange', requestUpdate);

    // small intersection observer to reduce work when out of view
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        const i = states.find(s => s.el === en.target);
        if (!i) return;
        if (en.isIntersecting) {
          // ensure it's updated
          requestUpdate();
        }
      });
    }, { root: null, threshold: [0, 0.25, 0.5, 0.75, 1] });

    states.forEach(s => obs.observe(s.el));
  });
})();
