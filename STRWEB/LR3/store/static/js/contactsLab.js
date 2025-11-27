class ContactsTable {
  constructor(root) {
    if (!root) return;
    this.root = root;
    this.apiUrl = root.dataset.api;

    this.tbody = root.querySelector("#contactsBody");
    this.pagination = root.querySelector("#pagination");
    this.preloader = root.querySelector("#labPreloader");
    this.filterInput = root.querySelector("#filterInput");
    this.filterButton = root.querySelector("#filterButton");
    this.resetFilterButton = root.querySelector("#resetFilter");
    this.addToggleButton = root.querySelector("#addToggle");
    this.rewardButton = root.querySelector("#rewardButton");
    this.selectAllCheckbox = root.querySelector("#selectAll");
    this.detailCard = root.querySelector("#detailCard");
    this.rewardOutput = root.querySelector("#rewardOutput");
    this.addSection = root.querySelector("#addSection");
    this.addForm = root.querySelector("#addForm");
    this.addSubmit = root.querySelector("#addSubmit");
    this.addCancel = root.querySelector("#addCancel");
    this.formStatus = root.querySelector("#formStatus");

    this.data = [];
    this.filtered = [];
    this.currentPage = 1;
    this.pageSize = 3;
    this.sortKey = null;
    this.sortDir = "asc";
    this.selectedIds = new Set();
    this.nextId = 10000;

    this.init();
  }

  init() {
    this.attachEvents();
    this.loadData();
  }

  showPreloader() {
    if (this.preloader) {
      this.preloader.classList.remove("hidden");
    }
  }

  hidePreloader() {
    if (this.preloader) {
      this.preloader.classList.add("hidden");
    }
  }

  async loadData() {
    if (!this.apiUrl) return;
    this.showPreloader();
    try {
      const resp = await fetch(this.apiUrl, { headers: { "X-Requested-With": "XMLHttpRequest" } });
      const payload = await resp.json();
      this.data = Array.isArray(payload.contacts) ? payload.contacts : [];
      this.filtered = [...this.data];
      this.currentPage = 1;
      this.applySort();
      this.render();
    } catch (e) {
      if (this.tbody) {
        this.tbody.innerHTML = `<tr><td colspan="6" class="placeholder-cell">Ошибка загрузки данных</td></tr>`;
      }
    } finally {
      this.hidePreloader();
    }
  }

  attachEvents() {
    const thead = this.root.querySelector("thead");
    if (thead) {
      thead.addEventListener("click", (e) => {
        const th = e.target.closest(".sortable");
        if (!th) return;
        const key = th.dataset.key;
        if (!key) return;
        if (this.sortKey === key) {
          this.sortDir = this.sortDir === "asc" ? "desc" : "asc";
        } else {
          this.sortKey = key;
          this.sortDir = "asc";
        }
        this.applySort();
        this.currentPage = 1;
        this.updateSortIndicators();
        this.render();
      });
    }

    if (this.filterButton) {
      this.filterButton.addEventListener("click", () => this.handleFilter());
    }
    if (this.resetFilterButton) {
      this.resetFilterButton.addEventListener("click", () => this.resetFilter());
    }

    if (this.tbody) {
      this.tbody.addEventListener("click", (e) => {
        const checkbox = e.target.closest("input[type='checkbox']");
        if (checkbox) {
          const tr = checkbox.closest("tr");
          if (!tr) return;
          const id = tr.dataset.id;
          this.toggleSelection(id, checkbox.checked);
          e.stopPropagation();
          return;
        }
        const row = e.target.closest("tr[data-id]");
        if (!row) return;
        const id = row.dataset.id;
        this.showDetails(id);
      });
    }

    if (this.selectAllCheckbox) {
      this.selectAllCheckbox.addEventListener("change", () => {
        this.toggleSelectAll(this.selectAllCheckbox.checked);
      });
    }

    if (this.rewardButton) {
      this.rewardButton.addEventListener("click", () => this.generateRewardText());
    }

    if (this.addToggleButton && this.addSection) {
      this.addToggleButton.addEventListener("click", () => {
        const visible = this.addSection.classList.toggle("is-visible");
        this.addSection.setAttribute("aria-hidden", visible ? "false" : "true");
      });
    }

    if (this.addCancel && this.addSection && this.addForm) {
      this.addCancel.addEventListener("click", () => {
        this.addSection.classList.remove("is-visible");
        this.addSection.setAttribute("aria-hidden", "true");
        this.addForm.reset();
        this.clearFormState();
      });
    }

    if (this.addForm) {
      this.addForm.addEventListener("input", () => this.validateForm());
      this.addForm.addEventListener("submit", (e) => {
        e.preventDefault();
        this.handleAdd();
      });
    }
  }

  applySort() {
    if (!this.sortKey) return;
    const dir = this.sortDir === "asc" ? 1 : -1;
    this.filtered.sort((a, b) => {
      const av = (a[this.sortKey] || "").toString().toLowerCase();
      const bv = (b[this.sortKey] || "").toString().toLowerCase();
      if (av < bv) return -1 * dir;
      if (av > bv) return 1 * dir;
      return 0;
    });
  }

  updateSortIndicators() {
    const headers = this.root.querySelectorAll(".sortable");
    headers.forEach((th) => {
      if (th.dataset.key === this.sortKey) {
        th.dataset.direction = this.sortDir;
      } else {
        th.removeAttribute("data-direction");
      }
    });
  }

  handleFilter() {
    if (!this.filterInput) return;
    const query = this.filterInput.value.trim().toLowerCase();
    this.showPreloader();
    setTimeout(() => {
      if (!query) {
        this.filtered = [...this.data];
      } else {
        this.filtered = this.data.filter((row) => {
          const fields = [row.name, row.role, row.phone, row.email];
          return fields.some((val) => (val || "").toString().toLowerCase().includes(query));
        });
      }
      this.currentPage = 1;
      this.applySort();
      this.render();
      this.hidePreloader();
    }, 200);
  }

  resetFilter() {
    if (this.filterInput) this.filterInput.value = "";
    this.filtered = [...this.data];
    this.currentPage = 1;
    this.applySort();
    this.render();
  }

  get totalPages() {
    if (!this.filtered.length) return 1;
    return Math.max(1, Math.ceil(this.filtered.length / this.pageSize));
  }

  render() {
    this.renderTable();
    this.renderPagination();
    this.syncSelectionState();
  }

  renderTable() {
    if (!this.tbody) return;
    if (!this.filtered.length) {
      this.tbody.innerHTML = `<tr><td colspan="6" class="placeholder-cell">Нет данных для отображения</td></tr>`;
      return;
    }
    const start = (this.currentPage - 1) * this.pageSize;
    const end = start + this.pageSize;
    const slice = this.filtered.slice(start, end);

    this.tbody.innerHTML = slice
      .map((row) => {
        const checked = this.selectedIds.has(String(row.id)) ? "checked" : "";
        return `
          <tr data-id="${row.id}">
            <td class="checkbox-col">
              <input type="checkbox" class="row-check" ${checked} />
            </td>
            <td>${row.name || ""}</td>
            <td>${row.role || ""}</td>
            <td>${row.phone || ""}</td>
            <td>${row.email || ""}</td>
            <td><img src="${row.photo || ""}" alt="${row.name || "Сотрудник"}"></td>
          </tr>
        `;
      })
      .join("");
  }

  renderPagination() {
    if (!this.pagination) return;
    const pages = this.totalPages;
    if (pages <= 1) {
      this.pagination.innerHTML = "";
      return;
    }
    let html = "";
    for (let i = 1; i <= pages; i++) {
      html += `<button type="button" class="${i === this.currentPage ? "is-active" : ""}" data-page="${i}">${i}</button>`;
    }
    this.pagination.innerHTML = html;
    this.pagination.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => {
        const page = Number(btn.dataset.page);
        if (!isNaN(page)) {
          this.currentPage = page;
          this.renderTable();
          this.syncSelectionState();
          this.renderPagination();
        }
      });
    });
  }

  findRowById(id) {
    return this.data.find((row) => String(row.id) === String(id));
  }

  showDetails(id) {
    const row = this.findRowById(id);
    if (!row || !this.detailCard) return;
    this.detailCard.innerHTML = `
      <img src="${row.photo || ""}" alt="${row.name || "Сотрудник"}">
      <div>
        <h3>${row.name || ""}</h3>
        <p class="meta">${row.role || ""}</p>
        <p>📞 ${row.phone || "—"}<br>✉️ ${row.email || "—"}</p>
        <p>${row.description || ""}</p>
      </div>
    `;
  }

  toggleSelection(id, isChecked) {
    if (!id) return;
    const key = String(id);
    if (isChecked) {
      this.selectedIds.add(key);
    } else {
      this.selectedIds.delete(key);
    }
    this.updateRewardState();
    this.updateSelectAllForPage();
  }

  toggleSelectAll(checked) {
    const start = (this.currentPage - 1) * this.pageSize;
    const end = start + this.pageSize;
    const slice = this.filtered.slice(start, end);
    slice.forEach((row) => {
      const id = String(row.id);
      if (checked) {
        this.selectedIds.add(id);
      } else {
        this.selectedIds.delete(id);
      }
    });
    this.renderTable();
    this.updateRewardState();
  }

  updateSelectAllForPage() {
    if (!this.selectAllCheckbox) return;
    const start = (this.currentPage - 1) * this.pageSize;
    const end = start + this.pageSize;
    const slice = this.filtered.slice(start, end);
    const allSelected =
      slice.length > 0 &&
      slice.every((row) => this.selectedIds.has(String(row.id)));
    this.selectAllCheckbox.checked = allSelected;
  }

  syncSelectionState() {
    if (!this.tbody) return;
    this.tbody.querySelectorAll("tr[data-id]").forEach((tr) => {
      const id = tr.dataset.id;
      const checked = this.selectedIds.has(String(id));
      const cb = tr.querySelector("input.row-check");
      if (cb) cb.checked = checked;
    });
    this.updateSelectAllForPage();
    this.updateRewardState();
  }

  updateRewardState() {
    if (!this.rewardButton) return;
    this.rewardButton.disabled = this.selectedIds.size === 0;
  }

  generateRewardText() {
    if (!this.rewardOutput || this.selectedIds.size === 0) return;
    const names = [];
    this.selectedIds.forEach((id) => {
      const row = this.findRowById(id);
      if (row && row.name) {
        const surname = row.name.split(" ")[0];
        names.push(surname);
      }
    });
    if (!names.length) {
      this.rewardOutput.textContent = "Сотрудники для премирования не выбраны.";
      return;
    }
    const list = names.join(", ");
    this.rewardOutput.textContent =
      `Предлагается премировать следующих сотрудников: ${list}. ` +
      `Основание: успешное выполнение задач и высокий уровень клиентского сервиса.`;
  }

  isValidUrl(url) {
    if (!url) return false;
    const re = /^https?:\/\/.+\.(php|html)(\/.*)?$/i;
    return re.test(url.trim());
  }

  isValidPhone(phone) {
    if (!phone) return false;
    const cleaned = phone.trim();
    const re = /^(?:\+375|8)\s*\(?\d{2,3}\)?(?:[\s-]*\d){7}$/;
    return re.test(cleaned);
  }

  validateForm() {
    if (!this.addForm || !this.addSubmit) return;
    const form = this.addForm;
    const name = form.elements["name"];
    const role = form.elements["role"];
    const description = form.elements["description"];
    const phone = form.elements["phone"];
    const email = form.elements["email"];
    const profileUrl = form.elements["profile_url"];
    const photo = form.elements["photo"];

    const phoneHint = this.root.querySelector('[data-hint="phone"]');
    const urlHint = this.root.querySelector('[data-hint="url"]');

    const markField = (field, isValid) => {
      field.classList.toggle("invalid-field", !isValid);
    };

    const requiredOk =
      name.value.trim().length >= 3 &&
      role.value.trim().length > 0 &&
      description.value.trim().length > 0 &&
      phone.value.trim().length > 0 &&
      email.value.trim().length > 0 &&
      profileUrl.value.trim().length > 0 &&
      photo.value.trim().length > 0;

    const phoneValid = this.isValidPhone(phone.value);
    const urlValid = this.isValidUrl(profileUrl.value);

    if (phoneHint) {
      phoneHint.textContent = phone.value
        ? phoneValid
          ? "Телефон валиден"
          : "Телефон не соответствует формату"
        : "";
    }
    if (urlHint) {
      urlHint.textContent = profileUrl.value
        ? urlValid
          ? "URL валиден"
          : "URL должен начинаться с http(s) и заканчиваться на .php или .html"
        : "";
    }

    markField(phone, !phoneValid && phone.value.trim().length > 0);
    markField(profileUrl, !urlValid && profileUrl.value.trim().length > 0);

    this.addSubmit.disabled = !(requiredOk && phoneValid && urlValid);
  }

  clearFormState() {
    if (!this.addForm) return;
    this.addForm
      .querySelectorAll(".invalid-field")
      .forEach((el) => el.classList.remove("invalid-field"));
    const phoneHint = this.root.querySelector('[data-hint="phone"]');
    const urlHint = this.root.querySelector('[data-hint="url"]');
    if (phoneHint) phoneHint.textContent = "";
    if (urlHint) urlHint.textContent = "";
    if (this.formStatus) this.formStatus.textContent = "";
    if (this.addSubmit) this.addSubmit.disabled = true;
  }

  handleAdd() {
    if (!this.addForm || !this.addSubmit) return;
    if (this.addSubmit.disabled) return;

    const form = this.addForm;
    const payload = {
      id: this.nextId++,
      name: form.elements["name"].value.trim(),
      role: form.elements["role"].value.trim(),
      description: form.elements["description"].value.trim(),
      phone: form.elements["phone"].value.trim(),
      email: form.elements["email"].value.trim(),
      photo: form.elements["photo"].value.trim(),
    };

    this.showPreloader();
    setTimeout(() => {
      this.data.push(payload);
      this.filtered = [...this.data];
      this.applySort();
      this.currentPage = this.totalPages;
      this.render();
      this.hidePreloader();

      if (this.formStatus) {
        this.formStatus.textContent = "Сотрудник добавлен в таблицу (клиентская вставка).";
      }
      this.addSubmit.disabled = true;
    }, 250);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const root = document.getElementById("contactsLabRoot");
  if (root) {
    new ContactsTable(root);
  }
});


