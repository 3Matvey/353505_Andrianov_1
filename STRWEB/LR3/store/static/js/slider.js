class ZooSlider {
  constructor(root, options = {}) {
    if (!root) {
      throw new Error("Slider root element is required");
    }
    this.root = root;
    this.track = root.querySelector(".slider-track");
    this.slides = Array.from(root.querySelectorAll("[data-slide]"));
    this.prevBtn = root.querySelector("[data-prev]");
    this.nextBtn = root.querySelector("[data-next]");
    this.pagination = root.querySelector("[data-pagination]");
    this.currentCounter = root.querySelector("[data-current]");
    this.totalCounter = root.querySelector("[data-total]");
    this.hoverArea = root;
    this.state = {
      index: 0,
      timer: null,
    };
    this.options = {
      loop: true,
      navs: true,
      pags: true,
      auto: true,
      stopMouseHover: true,
      delay: 5,
      ...options,
    };
    this.totalCounter.textContent = this.slides.length;
    this.init();
  }

  init() {
    this.renderPagination();
    this.bindEvents();
    this.applyOptionVisibility();
    this.updateUI();
    this.startAuto();
  }

  bindEvents() {
    if (this.prevBtn) {
      this.prevBtn.addEventListener("click", () => this.prev());
    }
    if (this.nextBtn) {
      this.nextBtn.addEventListener("click", () => this.next());
    }
    if (this.hoverArea) {
      this.hoverArea.addEventListener("mouseenter", () => {
        if (this.options.auto && this.options.stopMouseHover) {
          this.stopAuto();
        }
      });
      this.hoverArea.addEventListener("mouseleave", () => {
        if (this.options.auto && this.options.stopMouseHover) {
          this.startAuto();
        }
      });
    }
  }

  renderPagination() {
    if (!this.pagination) {
      return;
    }
    this.pagination.innerHTML = "";
    this.dots = this.slides.map((_, index) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.className = "slider-dot";
      dot.setAttribute("aria-label", `Перейти к слайду ${index + 1}`);
      dot.addEventListener("click", () => this.goTo(index));
      this.pagination.appendChild(dot);
      return dot;
    });
  }

  applyOptionVisibility() {
    if (this.prevBtn && this.nextBtn) {
      const display = this.options.navs ? "" : "none";
      this.prevBtn.style.display = display;
      this.nextBtn.style.display = display;
    }
    if (this.pagination) {
      this.pagination.style.display = this.options.pags ? "" : "none";
    }
  }

  updateOptions(newOptions = {}) {
    const merged = {
      ...this.options,
      ...newOptions,
    };
    if (!merged.auto) {
      merged.stopMouseHover = false;
    }
    this.options = merged;
    this.applyOptionVisibility();
    this.startAuto();
  }

  next() {
    this.goTo(this.state.index + 1);
  }

  prev() {
    this.goTo(this.state.index - 1);
  }

  goTo(targetIndex) {
    const maxIndex = this.slides.length - 1;
    let nextIndex = targetIndex;

    if (targetIndex < 0) {
      nextIndex = this.options.loop ? maxIndex : 0;
    } else if (targetIndex > maxIndex) {
      nextIndex = this.options.loop ? 0 : maxIndex;
    }

    this.state.index = nextIndex;
    this.updateUI();
  }

  updateUI() {
    const offset = -this.state.index * 100;
    this.track.style.transform = `translateX(${offset}%)`;

    if (this.currentCounter) {
      this.currentCounter.textContent = this.state.index + 1;
    }

    if (this.dots) {
      this.dots.forEach((dot, idx) => {
        dot.classList.toggle("is-active", idx === this.state.index);
      });
    }
  }

  startAuto() {
    this.stopAuto();
    if (!this.options.auto) {
      return;
    }
    const delayMs = Math.max(1, Number(this.options.delay) || 5) * 1000;
    this.state.timer = setInterval(() => this.next(), delayMs);
  }

  stopAuto() {
    if (this.state.timer) {
      clearInterval(this.state.timer);
      this.state.timer = null;
    }
  }
}

window.ZooSlider = ZooSlider;

