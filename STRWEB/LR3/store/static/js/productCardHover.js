// Small tilt / parallax effect for product cards
// Applies transform on .product-item based on mouse position

(function(){
  const rootSelector = '.products-grid';
  const cardSelector = '.product-item';
  const maxRotate = 10; // degrees
  const maxTranslate = 12; // px for subtle Z translate effect

  function handlePointerMove(e, card, rect) {
    const px = (e.clientX - rect.left) / rect.width; // 0..1
    const py = (e.clientY - rect.top) / rect.height; // 0..1

    const rotateY = (px - 0.5) * 2 * maxRotate * -1; // invert to follow cursor
    const rotateX = (py - 0.5) * 2 * maxRotate;
    const translateZ = (0.5 - Math.abs(px - 0.5)) * maxTranslate + (0.5 - Math.abs(py - 0.5)) * maxTranslate;

    card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(${translateZ}px)`;
    card.classList.add('is-tilting');
  }

  function resetCard(card) {
    card.style.transform = '';
    card.classList.remove('is-tilting');
  }

  function attachToGrid(grid) {
    if (!grid) return;
    let active = null;

    grid.addEventListener('pointerenter', (e) => {
      const card = e.target.closest(cardSelector);
      if (!card) return;
      // ensure pointer capture on the card
      card.setPointerCapture?.(e.pointerId);
    }, {capture: true});

    grid.addEventListener('pointermove', (e) => {
      const card = e.target.closest(cardSelector);
      if (!card) return;
      const rect = card.getBoundingClientRect();
      handlePointerMove(e, card, rect);
    });

    grid.addEventListener('pointerleave', (e) => {
      const card = e.target.closest(cardSelector);
      if (card) resetCard(card);
      // If leaving grid entirely, reset any remaining cards
      if (!grid.contains(e.relatedTarget)) {
        grid.querySelectorAll(cardSelector).forEach(c => resetCard(c));
      }
    });

    // touch support: reset on touchend
    grid.addEventListener('touchend', (e) => {
      grid.querySelectorAll(cardSelector).forEach(c => resetCard(c));
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    const grid = document.querySelector(rootSelector);
    attachToGrid(grid);
  });
})();
