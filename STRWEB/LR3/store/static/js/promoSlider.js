class PromoSlider {
  constructor(root, options = {}) {
    if (!root) {
      throw new Error('PromoSlider root element is required');
    }

    this.root = root;
    this.viewport = root.querySelector('.promo-slider__viewport');
    this.slides = Array.from(root.querySelectorAll('.promo-slide'));
    this.navPrev = root.querySelector('[data-slider-prev]');
    this.navNext = root.querySelector('[data-slider-next]');
    this.paginationContainer = root.querySelector('[data-slider-pagination]');
    this.counterCurrent = root.querySelector('[data-slider-current]');
    this.counterTotal = root.querySelector('[data-slider-total]');

    this.currentIndex = -1;
    this.total = this.slides.length;
    this.paginationDots = [];
    this.autoTimer = null;
    this.isHovered = false;

    const datasetOptions = this.parseDataset();
    this.options = Object.assign(
      {
        loop: true,
        navs: true,
        pags: true,
        auto: true,
        stopHover: true,
        delay: 5000,
      },
      datasetOptions,
      options,
    );

    this.init();
  }

  parseDataset() {
    const { dataset } = this.root;
    return {
      loop: this.parseBoolean(dataset.loop, true),
      navs: this.parseBoolean(dataset.navs, true),
      pags: this.parseBoolean(dataset.pags, true),
      auto: this.parseBoolean(dataset.auto, true),
      stopHover: this.parseBoolean(dataset.stopHover, true),
      delay: this.parseDelay(dataset.delay, 5),
    };
  }

  parseBoolean(value, fallback) {
    if (typeof value === 'undefined') {
      return fallback;
    }
    return String(value).toLowerCase() === 'true';
  }

  parseDelay(value, fallbackSeconds) {
    const seconds = Number(value);
    const safeSeconds = Number.isFinite(seconds) && seconds > 0 ? seconds : fallbackSeconds;
    return safeSeconds * 1000;
  }

  init() {
    if (!this.viewport || this.total === 0) {
      return;
    }

    if (this.counterTotal) {
      this.counterTotal.textContent = this.total;
    }

    this.buildPagination();
    this.bindEvents();
    this.goToSlide(0, false);
    this.toggleNavVisibility();
    this.togglePaginationVisibility();
    this.startAuto();
  }

  bindEvents() {
    if (this.navPrev) {
      this.navPrev.addEventListener('click', () => this.prev());
    }

    if (this.navNext) {
      this.navNext.addEventListener('click', () => this.next());
    }

    if (this.options.stopHover) {
      this.root.addEventListener('mouseenter', () => {
        this.isHovered = true;
        this.stopAuto();
      });

      this.root.addEventListener('mouseleave', () => {
        this.isHovered = false;
        this.startAuto();
      });
    }
  }

  buildPagination() {
    if (!this.paginationContainer) {
      return;
    }
    this.paginationContainer.innerHTML = '';

    this.paginationDots = this.slides.map((_, index) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'promo-slider__dot';
      dot.setAttribute('aria-label', `Перейти к слайду ${index + 1}`);
      dot.addEventListener('click', () => this.goToSlide(index));
      this.paginationContainer.appendChild(dot);
      return dot;
    });
  }

  toggleNavVisibility() {
    const showNavs = this.options.navs && this.total > 1;
    [this.navPrev, this.navNext].forEach((nav) => {
      if (!nav) {
        return;
      }
      nav.style.display = showNavs ? 'grid' : 'none';
    });
  }

  togglePaginationVisibility() {
    if (!this.paginationContainer) {
      return;
    }
    const display = this.options.pags && this.total > 1 ? 'flex' : 'none';
    this.paginationContainer.style.display = display;
  }

  goToSlide(index, restartAuto = true) {
    if (this.total === 0) {
      return;
    }

    const clampedIndex = this.getValidIndex(index);
    if (clampedIndex === this.currentIndex) {
      return;
    }

    this.currentIndex = clampedIndex;
    this.updateViewportPosition();
    this.updateCounter();
    this.updatePaginationState();

    if (restartAuto) {
      this.startAuto();
    }
  }

  getValidIndex(index) {
    if (this.options.loop) {
      const loopedIndex = (index + this.total) % this.total;
      return loopedIndex;
    }
    return Math.max(0, Math.min(index, this.total - 1));
  }

  updateViewportPosition() {
    const offset = this.currentIndex * -100;
    this.viewport.style.transform = `translateX(${offset}%)`;
  }

  updateCounter() {
    if (this.counterCurrent) {
      this.counterCurrent.textContent = this.currentIndex + 1;
    }
  }

  updatePaginationState() {
    if (!this.paginationDots.length) {
      return;
    }
    this.paginationDots.forEach((dot, idx) => {
      dot.classList.toggle('is-active', idx === this.currentIndex);
      dot.setAttribute('aria-current', idx === this.currentIndex ? 'true' : 'false');
    });
  }

  next() {
    const targetIndex = this.options.loop ? this.currentIndex + 1 : Math.min(this.currentIndex + 1, this.total - 1);
    this.goToSlide(targetIndex);
  }

  prev() {
    const targetIndex = this.options.loop ? this.currentIndex - 1 : Math.max(this.currentIndex - 1, 0);
    this.goToSlide(targetIndex);
  }

  startAuto() {
    if (!this.options.auto || this.total <= 1 || this.isHovered) {
      return;
    }
    this.stopAuto();
    this.autoTimer = window.setTimeout(() => {
      this.next();
      this.startAuto();
    }, this.options.delay);
  }

  stopAuto() {
    if (this.autoTimer) {
      window.clearTimeout(this.autoTimer);
      this.autoTimer = null;
    }
  }

  setDelay(seconds) {
    const safeSeconds = Number(seconds);
    if (!Number.isFinite(safeSeconds) || safeSeconds <= 0) {
      return;
    }
    this.options.delay = safeSeconds * 1000;
    if (this.options.auto) {
      this.startAuto();
    }
  }
}

window.PromoSlider = PromoSlider;

