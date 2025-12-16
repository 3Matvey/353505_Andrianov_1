// parallaxAbout.js — simple multi-layer parallax for the about page hero
(function(){
  'use strict';

  function $(sel){ return document.querySelector(sel); }

  function clamp(v, a, b){ return Math.max(a, Math.min(b, v)); }

  document.addEventListener('DOMContentLoaded', function(){
    const bg = $('#bg');
    const text = $('#text');
    const parrot = $('#parrot');
    const clouds1 = $('#clouds_1');
    const clouds2 = $('#clouds_2');
    // collect parrot layers (these will fly up on scroll)
    const parrots = Array.from(document.querySelectorAll('.parrot-layer'));
    const gif = $('#gifParrot');
    let gifPlaying = false;
    const gifOriginalSrc = gif ? gif.src : null;

    if (!bg && !parrot && !clouds1 && !clouds2 && parrots.length === 0) return;

    const hero = document.getElementById('top');

    function onScroll(){
      const rect = hero.getBoundingClientRect();
      const progress = clamp(-rect.top / rect.height, 0, 1); // 0..1 as hero scrolls off
      const maxOffset = 320; // max vertical movement for layers
      const maxMain = 180; // max move for main parrot
      const maxRot = 18; // max degrees rotation for layers

      // clouds: gentle horizontal displacement based on progress
      if (clouds1) clouds1.style.transform = `translate3d(${progress * 120}px,0,0)`;
      if (clouds2) clouds2.style.transform = `translate3d(${ -progress * 80 }px,0,0)`;

      // main parrot: translate up and slightly scale down
      if (parrot) {
        const offsetM = -progress * maxMain;
        const scale = 1 - Math.min(0.18, progress * 0.18);
        parrot.style.transform = `translate3d(-50%, ${offsetM}px, 0) scale(${scale})`;
        parrot.style.opacity = `${1 - progress * 0.05}`;
      }

      // headline: move up a bit for depth
      if (text) text.style.transform = `translate3d(0, ${ -progress * 40 }px, 0)`;

      // each parrot layer flies up with limits
      parrots.forEach((p, i) => {
        const speed = Number(p.dataset.speed) || 0.45;
        const offset = -Math.min(maxOffset, progress * maxOffset * speed);
        const rot = (offset / maxOffset) * maxRot * (i % 2 === 0 ? 1 : -1);
        // if element should be mirrored horizontally, append scaleX(-1)
        const mirror = p.dataset.mirror === 'true' || p.classList.contains('mirrored');
        const mirrorSuffix = mirror ? ' scaleX(-1)' : '';
        p.style.transform = `translate3d(0, ${offset}px, 0) rotate(${rot}deg)${mirrorSuffix}`;
        const opacity = Math.max(0.12, 1 - Math.abs(offset) / (maxOffset * 1.1));
        p.style.opacity = opacity;
      });

      // GIF parrot: restart its animation when entering view and animate upward
      if (gif) {
        const threshold = 0.12; // when hero scrolled enough to trigger
        const speed = Number(gif.dataset.speed) || 0.7;
        const gifOffset = -Math.min(maxOffset * 1.2, progress * maxOffset * 1.3 * speed);
        const gifMirror = gif.dataset.mirror === 'true' || gif.classList.contains('mirrored');
        const gifMirrorSuffix = gifMirror ? ' scaleX(-1)' : '';
        gif.style.transform = `translate3d(0, ${gifOffset}px, 0) scale(${1 - progress * 0.06})${gifMirrorSuffix}`;
        gif.style.opacity = `${Math.max(0.08, 1 - progress * 0.9)}`;

        // restart GIF when it first becomes visible (cross threshold); allow replay after scrolling back up
        if (progress > threshold && !gifPlaying) {
          // force reload/restart GIF by reassigning src with a timestamp
          try {
            gif.src = gifOriginalSrc + (gifOriginalSrc.indexOf('?') === -1 ? '?' : '&') + 'r=' + Date.now();
          } catch (e) {
            // fallback: assign same src
            gif.src = gifOriginalSrc;
          }
          gifPlaying = true;
        } else if (progress < 0.03 && gifPlaying) {
          // reset flag so GIF will replay next time user scrolls down
          gifPlaying = false;
        }
      }
    }

    // use passive scroll listener for performance
    window.addEventListener('scroll', onScroll, { passive: true });
    // initial
    onScroll();
  });
})();
