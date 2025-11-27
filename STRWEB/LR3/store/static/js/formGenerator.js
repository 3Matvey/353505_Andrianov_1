class FormElementGenerator {
  constructor(root) {
    if (!root) return;
    this.root = root;
    this.storageKey = "lab4_elements";
    this.toggle = root.querySelector("#formElementToggle");
    this.list = root.querySelector("#generatedElements");
    this.counter = 0;

    this.attachEvents();
    this.restore();
  }

  attachEvents() {
    if (this.toggle) {
      this.toggle.addEventListener("change", () => {
        if (this.toggle.checked) {
          this.addElement();
          this.toggle.checked = false;
        }
      });
    }
  }

  templateConfig() {
    return {
      id: `gen-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      label: "Пользовательское поле",
      placeholder: "Введите значение",
      min: 0,
      max: 100,
      step: 5,
      required: true,
    };
  }

  createElement(config) {
    const item = document.createElement("article");
    item.className = "generated-item";
    item.dataset.id = config.id;

    item.innerHTML = `
      <div class="generated-preview">
        <label>
          <span class="preview-label">${config.label}</span>
          <input type="range" min="${config.min}" max="${config.max}" step="${config.step}" placeholder="${config.placeholder}" ${config.required ? "required" : ""} />
        </label>
        <div class="preview-meta">min=${config.min} · max=${config.max} · step=${config.step} · ${config.required ? "обязательно" : "необязательно"}</div>
      </div>
      <div class="generated-controls">
        <label>Подпись<input type="text" name="label" value="${config.label}"></label>
        <label>Placeholder<input type="text" name="placeholder" value="${config.placeholder}"></label>
        <label>min<input type="number" name="min" min="0" max="1000" value="${config.min}"></label>
        <label>max<input type="number" name="max" min="1" max="2000" value="${config.max}"></label>
        <label>step<input type="number" name="step" min="1" max="500" value="${config.step}"></label>
        <label class="inline"><input type="checkbox" name="required" ${config.required ? "checked" : ""}> required</label>
        <button type="button" class="btn btn-outline-danger" data-remove>Удалить</button>
      </div>
    `;

    item.addEventListener("input", (e) => {
      const target = e.target;
      const name = target.name;
      if (!name) return;
      const newConfig = this.readConfig(item, config);
      this.updatePreview(item, newConfig);
      this.saveState();
    });

    const removeBtn = item.querySelector("[data-remove]");
    if (removeBtn) {
      removeBtn.addEventListener("click", () => {
        item.remove();
        this.saveState();
      });
    }

    return item;
  }

  readConfig(item, fallback) {
    const get = (selector, mapper = (v) => v) => {
      const field = item.querySelector(selector);
      return field ? mapper(field.value) : null;
    };

    const min = Number(get("input[name='min']")) || 0;
    const max = Number(get("input[name='max']")) || 0;
    const step = Number(get("input[name='step']")) || 1;
    const required = !!item.querySelector("input[name='required']")?.checked;

    return {
      ...fallback,
      label: get("input[name='label']") || fallback.label,
      placeholder: get("input[name='placeholder']") || fallback.placeholder,
      min: min > 0 ? min : 0,
      max: max > min ? max : min + 1,
      step: step > 0 ? step : 1,
      required,
    };
  }

  updatePreview(item, config) {
    const labelEl = item.querySelector(".preview-label");
    const inputEl = item.querySelector("input[type='range']");
    const metaEl = item.querySelector(".preview-meta");
    if (labelEl) labelEl.textContent = config.label;
    if (inputEl) {
      inputEl.min = config.min;
      inputEl.max = config.max;
      inputEl.step = config.step;
      inputEl.placeholder = config.placeholder;
      inputEl.required = config.required;
    }
    if (metaEl) {
      metaEl.textContent = `min=${config.min} · max=${config.max} · step=${config.step} · ${config.required ? "обязательно" : "необязательно"}`;
    }
    item.dataset.config = JSON.stringify(config);
  }

  addElement(config = null) {
    const cfg = config || this.templateConfig();
    const item = this.createElement(cfg);
    this.updatePreview(item, cfg);
    if (this.list) {
      this.list.appendChild(item);
    }
    this.saveState();
  }

  saveState() {
    if (!this.list) return;
    const data = [];
    this.list.querySelectorAll(".generated-item").forEach((item) => {
      const stored = item.dataset.config;
      if (stored) {
        try {
          data.push(JSON.parse(stored));
        } catch (e) {
          // ignore
        }
      }
    });
    localStorage.setItem(this.storageKey, JSON.stringify(data));
  }

  restore() {
    const raw = localStorage.getItem(this.storageKey);
    if (!raw) return;
    try {
      const parsed = JSON.parse(raw);
      parsed.forEach((cfg) => this.addElement(cfg));
    } catch (e) {
      // ignore corrupted state
    }
  }
}

window.addEventListener("DOMContentLoaded", () => {
  const root = document.getElementById("formGenerator");
  if (root) {
    new FormElementGenerator(root);
  }
});
