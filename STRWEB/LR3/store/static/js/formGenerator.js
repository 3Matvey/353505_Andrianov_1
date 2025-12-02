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
      name: `input_${this.counter++}`,
      placeholder: "Введите значение",
      maxlength: 50,
      value: "",
      readonly: false,
      disabled: false,
    };
  }

  createElement(config) {
    const item = document.createElement("article");
    item.className = "generated-item";
    item.dataset.id = config.id;

    const readonlyAttr = config.readonly ? 'readonly' : '';
    const disabledAttr = config.disabled ? 'disabled' : '';

    item.innerHTML = `
      <div class="generated-preview">
        <label>
          <span class="preview-label">Поле: <code>${config.name}</code></span>
          <input type="text" placeholder="${config.placeholder}" maxlength="${config.maxlength}" value="${config.value}" ${readonlyAttr} ${disabledAttr} />
        </label>
        <div class="preview-meta">maxlength=${config.maxlength} · ${config.readonly ? "readonly" : ""} ${config.disabled ? "disabled" : ""}</div>
      </div>
      <div class="generated-controls">
        <label>name<input type="text" name="name" value="${config.name}"></label>
        <label>placeholder<input type="text" name="placeholder" value="${config.placeholder}"></label>
        <label>maxlength<input type="number" name="maxlength" min="1" max="500" value="${config.maxlength}"></label>
        <label>value<input type="text" name="value" value="${config.value}"></label>
        <label class="inline"><input type="checkbox" name="readonly" ${config.readonly ? "checked" : ""}> readonly</label>
        <label class="inline"><input type="checkbox" name="disabled" ${config.disabled ? "checked" : ""}> disabled</label>
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

    const maxlength = Number(get("input[name='maxlength']")) || 50;
    const readonly = !!item.querySelector("input[name='readonly']")?.checked;
    const disabled = !!item.querySelector("input[name='disabled']")?.checked;

    return {
      ...fallback,
      name: get("input[name='name']") || fallback.name,
      placeholder: get("input[name='placeholder']") || fallback.placeholder,
      maxlength: maxlength > 0 ? maxlength : 50,
      value: get("input[name='value']") || fallback.value,
      readonly,
      disabled,
    };
  }

  updatePreview(item, config) {
    const labelEl = item.querySelector(".preview-label");
    const inputEl = item.querySelector("input[type='text']");
    const metaEl = item.querySelector(".preview-meta");
    
    if (labelEl) labelEl.innerHTML = `Поле: <code>${config.name}</code>`;
    if (inputEl) {
      inputEl.placeholder = config.placeholder;
      inputEl.maxLength = config.maxlength;
      inputEl.value = config.value;
      inputEl.readOnly = config.readonly;
      inputEl.disabled = config.disabled;
    }
    if (metaEl) {
      const flags = [
        `maxlength=${config.maxlength}`,
        config.readonly ? "readonly" : null,
        config.disabled ? "disabled" : null,
      ].filter(Boolean).join(" · ");
      metaEl.textContent = flags;
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
