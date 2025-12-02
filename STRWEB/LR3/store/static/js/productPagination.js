/* Client-side product pagination
	 - reads products JSON from `data-products` on root `#productPaginationRoot`
	 - renders products into `#productContainer`
	 - renders pagination into `#paginationNav`
	 - supports page size select `#pageSize` (3,5,10)
	 - saves current page & pageSize to localStorage to persist across reloads
*/

class ProductPagination {
	constructor(root) {
		if (!root) return;
		this.root = root;
		this.container = document.getElementById('productContainer');
		this.paginationNav = document.getElementById('paginationNav');
		this.pageSizeSelect = document.getElementById('pageSize');
		this.storageKey = 'productPaginationState';

		this.allProducts = [];
		this.endpoint = root.getAttribute('data-endpoint') || null;
		const raw = root.getAttribute('data-products');
		if (raw) {
			try {
				this.allProducts = JSON.parse(raw);
			} catch (e) {
				this.allProducts = [];
				console.error('Failed to parse products JSON', e);
			}
		}

		this.currentPage = 1;
		this.pageSize = 3;

		this.init();
	}

	init() {
		this.attachEvents();
		this.restoreState();
		if (this.endpoint) {
			// fetch products from server (apply current querystring)
			const url = this.endpoint + window.location.search;
			fetch(url, { credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' } })
				.then(resp => resp.json())
				.then(data => {
					if (Array.isArray(data.products)) this.allProducts = data.products;
					// ensure currentPage is within range
					if (this.currentPage > this.totalPages) this.currentPage = 1;
					this.render();
				})
				.catch(err => {
					console.error('Failed to load products JSON', err);
					this.render();
				});
		} else {
			this.render();
		}
	}

	attachEvents() {
		if (this.pageSizeSelect) {
			this.pageSizeSelect.addEventListener('change', (e) => {
				const val = Number(e.target.value) || 3;
				this.pageSize = val;
				this.currentPage = 1;
				this.saveState();
				this.render();
			});
		}

		// handle clicks on pagination (delegate)
		if (this.paginationNav) {
			this.paginationNav.addEventListener('click', (e) => {
				const btn = e.target.closest('[data-page]');
				if (!btn) return;
				const page = Number(btn.dataset.page);
				if (!isNaN(page)) this.goToPage(page);
			});
		}
	}

	saveState() {
		try {
			localStorage.setItem(this.storageKey, JSON.stringify({
				page: this.currentPage,
				pageSize: this.pageSize
			}));
		} catch (e) {
			// ignore
		}
	}

	restoreState() {
		try {
			const raw = localStorage.getItem(this.storageKey);
			if (!raw) return;
			const s = JSON.parse(raw);
			if (s && s.pageSize) this.pageSize = Number(s.pageSize) || this.pageSize;
			if (s && s.page) this.currentPage = Number(s.page) || this.currentPage;
			if (this.pageSizeSelect) this.pageSizeSelect.value = String(this.pageSize);
		} catch (e) {
			// ignore
		}
	}

	get totalPages() {
		if (!Array.isArray(this.allProducts) || this.allProducts.length === 0) return 1;
		return Math.max(1, Math.ceil(this.allProducts.length / this.pageSize));
	}

	getCurrentPageProducts() {
		const start = (this.currentPage - 1) * this.pageSize;
		return this.allProducts.slice(start, start + this.pageSize);
	}

	goToPage(page) {
		if (page < 1) page = 1;
		if (page > this.totalPages) page = this.totalPages;
		if (page === this.currentPage) return;
		this.currentPage = page;
		this.saveState();
		this.render();
		// scroll to products
		if (this.container) this.container.scrollIntoView({ behavior: 'smooth', block: 'start' });
	}

	renderProducts() {
		if (!this.container) return;

		const list = this.getCurrentPageProducts();
		if (!list || list.length === 0) {
			this.container.innerHTML = '<div class="product-item">Товары не найдены.</div>';
			return;
		}

		this.container.innerHTML = list.map(p => {
			const sku = encodeURIComponent(p.sku || '');
			const name = this.escapeHtml(p.name || '');
			const cat = this.escapeHtml(p['category__name'] || '');
			const price = this.escapeHtml(String(p.price || ''));
			return `
				<article class="product-item" itemscope itemtype="https://schema.org/Product">
					<header>
						<a href="/products/${sku}/" itemprop="url">
							<h3 class="heading-transform" itemprop="name">${name}</h3>
						</a>
						<div class="small">(<span itemprop="category">${cat}</span>)</div>
						<meta itemprop="sku" content="${sku}">
					</header>
					<div class="price" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
						<span class="badge bg-primary rounded-pill"><span itemprop="price">${price}</span> <span itemprop="priceCurrency" content="BYN">р.</span></span>
						<link itemprop="availability" href="https://schema.org/InStock" />
					</div>
				</article>`;
		}).join('');
	}

	renderPagination() {
		if (!this.paginationNav) return;
		const pages = this.totalPages;
		if (pages <= 1) {
			this.paginationNav.innerHTML = '';
			return;
		}
		let html = '<ul class="pagination">';
		// prev
		if (this.currentPage > 1) {
			html += `<li class="page-item"><button type="button" class="page-link" data-page="${this.currentPage - 1}">←</button></li>`;
		} else {
			html += `<li class="page-item disabled"><span class="page-link">←</span></li>`;
		}
		// pages (limit display when many)
		const maxButtons = 7;
		let start = 1, end = pages;
		if (pages > maxButtons) {
			const half = Math.floor(maxButtons / 2);
			start = Math.max(1, this.currentPage - half);
			end = start + maxButtons - 1;
			if (end > pages) { end = pages; start = end - maxButtons + 1; }
		}
		for (let i = start; i <= end; i++) {
			if (i === this.currentPage) html += `<li class="page-item active"><span class="page-link">${i}</span></li>`;
			else html += `<li class="page-item"><button type="button" class="page-link" data-page="${i}">${i}</button></li>`;
		}
		// next
		if (this.currentPage < pages) {
			html += `<li class="page-item"><button type="button" class="page-link" data-page="${this.currentPage + 1}">→</button></li>`;
		} else {
			html += `<li class="page-item disabled"><span class="page-link">→</span></li>`;
		}
		html += '</ul>';
		this.paginationNav.innerHTML = html;
	}

	render() {
		this.renderProducts();
		this.renderPagination();
	}

	escapeHtml(str) {
		return String(str)
			.replace(/&/g, '&amp;')
			.replace(/</g, '&lt;')
			.replace(/>/g, '&gt;')
			.replace(/"/g, '&quot;')
			.replace(/'/g, '&#39;');
	}
}

document.addEventListener('DOMContentLoaded', () => {
	const root = document.getElementById('productPaginationRoot');
	if (root) new ProductPagination(root);
});

