import base64
import io
import json
import os
import re
from urllib.parse import urlsplit

from django.http import JsonResponse
from matplotlib import pyplot as plt
from django.core.files.base import ContentFile
from django.db.models.functions import TruncDate
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Count
from django.views.decorators.http import require_GET, require_http_methods
import requests
from django.utils import timezone

from .utils import fetch_nbrb_rates, fetch_exchange_rates
from zoo_shop import settings
from store.decorators import employee_required
from store.forms import CompanyNewsForm, ProfileForm, ReviewForm, SaleForm, SignUpForm
from store.models import CompanyNews, Product, Partner, Category, Sale, Supplier, Client, Employee, CompanyInfo, FAQ, Contact, Vacancy


def news(request):
    """
    Новости из БД с пагинацией и курсы валют
    """
    qs = CompanyNews.objects.order_by('-published_at')
    paginator = Paginator(qs, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    rates = fetch_nbrb_rates(symbols=['USD', 'EUR'])

    return render(request, 'store/news.html', {
        'page_obj': page_obj,
        'rates': rates,
    })



@login_required
@employee_required
def news_create(request):
    if request.method == 'POST':
        form = CompanyNewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Новость добавлена.")
            return redirect('news')
    else:
        form = CompanyNewsForm()

    return render(request, 'store/news_create.html', {'form': form})


@login_required
@employee_required
def news_update(request, pk):
    news_item = get_object_or_404(CompanyNews, pk=pk)

    if request.method == 'POST':
        form = CompanyNewsForm(request.POST, request.FILES, instance=news_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Новость обновлена.")
            return redirect('news')
    else:
        form = CompanyNewsForm(instance=news_item)

    return render(request, 'store/news_update.html', {'form': form, 'news_item': news_item})


@login_required
@employee_required
def news_delete(request, pk):
    news_item = get_object_or_404(CompanyNews, pk=pk)

    if request.method == 'POST':
        news_item.delete()
        messages.success(request, "Новость удалена.")
        return redirect('news')

    return render(request, 'store/news_delete.html', {'news_item': news_item})


@login_required
def news_detail(request, pk):
    news_item = get_object_or_404(CompanyNews, pk=pk)
    return render(request, 'store/news_detail.html', {
        'news_item': news_item
    })


def home(request):
    article = CompanyNews.objects.order_by('-published_at').first()
    user_time = timezone.localtime(timezone.now())
    # Баннеры (пути к картинкам)
    banners = [
        '/media/news/Снимок_экрана_1_FADhcEz.png',
        '/media/news/Снимок_экрана_1_jFjpZxv.png',
        '/media/news/Снимок_экрана_1_oktD0nW.png',
    ]
    # Краткий каталог товаров (первые 5)
    products = Product.objects.select_related('category').all()[:5]
    # Партнеры
    partners = Partner.objects.all()
    # Логотип (берем первый из CompanyInfo с заголовком "Логотип" или вручную)
    logo_block = CompanyInfo.objects.filter(title__icontains="логотип").first()
    logo_url = logo_block.content if logo_block else '/media/contacts/Снимок_экрана_1.png'

    return render(request, 'store/home.html', {
        'article': article,
        'user_time': user_time,
        'banners': banners,
        'products': products,
        'partners': partners,
        'logo_url': logo_url,
    })

def about(request):
    info_blocks = CompanyInfo.objects.all()
    return render(request, 'store/about.html', {
        'info_blocks': info_blocks
    })

def glossary(request):
    faqs = FAQ.objects.all()
    return render(request, 'store/glossary.html', {
        'faqs': faqs
    })

def contacts(request):
    people = Contact.objects.all()
    return render(request, 'store/contacts.html', {
        'people': people
    })


def contacts_lab(request):
    return render(request, 'store/contacts_lab.html')


@require_GET
def contacts_lab_data(request):
    """
    Возвращает JSON с сотрудниками из таблицы Contact.
    """
    contacts = [
        {
            "id": person.id,
            "name": person.name,
            "role": person.role or "",
            "description": person.description or "",
            "phone": person.phone or "",
            "email": person.email or "",
            "photo": request.build_absolute_uri(person.photo.url) if person.photo else "",
        }
        for person in Contact.objects.all()
    ]

    return JsonResponse({"contacts": contacts})


@require_http_methods(["POST"])
def contacts_lab_add(request):
    """Создаёт нового сотрудника в таблице Contact по данным из формы."""

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Некорректный формат данных."}, status=400)

    def fail(message, status=400):
        return JsonResponse({"error": message}, status=status)

    name = (payload.get("name") or "").strip()
    role = (payload.get("role") or "").strip()
    description = (payload.get("description") or "").strip()
    phone = (payload.get("phone") or "").strip()
    email = (payload.get("email") or "").strip()
    profile_url = (payload.get("profile_url") or "").strip()
    photo_url = (payload.get("photo_url") or "").strip()

    if not all([name, role, description, phone, email, profile_url, photo_url]):
        return fail("Пожалуйста, заполните все поля формы.")

    phone_re = re.compile(r"^(?:\+375|8)\s*\(?\d{2,3}\)?(?:[\s-]*\d){7}$")
    url_re = re.compile(r"^https?://.+\.(php|html)(/.*)?$", re.IGNORECASE)

    if not url_re.match(profile_url):
        return fail("URL профиля должен начинаться с http(s) и заканчиваться на .php или .html.")

    if not phone_re.match(phone):
        return fail("Телефон не соответствует требуемому формату.")

    try:
        photo_resp = requests.get(photo_url, timeout=8)
        photo_resp.raise_for_status()
    except Exception:
        return fail("Не удалось скачать фото по указанному URL.", status=422)

    filename = os.path.basename(urlsplit(photo_url).path) or "contact_photo.jpg"

    contact = Contact(
        name=name,
        role=role,
        description=description,
        phone=phone,
        email=email,
    )
    contact.photo.save(filename, ContentFile(photo_resp.content), save=False)
    contact.save()

    return JsonResponse(
        {
            "contact": {
                "id": contact.id,
                "name": contact.name,
                "role": contact.role,
                "description": contact.description,
                "phone": contact.phone,
                "email": contact.email,
                "photo": request.build_absolute_uri(contact.photo.url) if contact.photo else "",
            }
        },
        status=201,
    )

def privacy(request):
    return render(request, 'store/privacy.html')

def vacancies(request):
    vacs = Vacancy.objects.all()
    return render(request, 'store/vacancies.html', {
        'vacancies': vacs
    })

def promocodes(request):
    from .models import PromoCode
    active_promocodes = PromoCode.objects.filter(is_active=True)
    archived_promocodes = PromoCode.objects.filter(is_active=False)
    return render(request, 'store/promocodes.html', {
        'active_promocodes': active_promocodes,
        'archived_promocodes': archived_promocodes
    })


def slider_page(request):
    slides = [
        {
            "title": "Новинки для питомцев",
            "caption": "Лучшие лаки и лакомства недели",
            "image": "/media/news/Снимок_экрана_1_oktD0nW.png",
            "url": "/products/",
        },
        {
            "title": "События зоопарка",
            "caption": "Читайте свежие новости компании",
            "image": "/media/news/Снимок_экрана_2024-05-17_150737.png",
            "url": "/news/",
        },
        {
            "title": "Скидки на аксессуары",
            "caption": "Акции доступны до конца месяца",
            "image": "/media/news/Снимок_экрана_1_FADhcEz.png",
            "url": "/promocodes/",
        },
    ]
    return render(request, 'store/slider.html', {"slides": slides})


def students(request):
    """Page for managing school students and finding duplicates (both prototype and class-based inheritance)."""
    return render(request, 'store/students.html')


def chart_page(request):
    """Chart.js demo page for lab task: plots series approximation and exact function.

    Uses client-side JS to compute series terms and draw Chart.js graphs.
    """
    return render(request, 'store/chart.html')


def is_employee_or_super(user):
    return user.is_superuser or hasattr(user, "employee_profile")


@login_required
@user_passes_test(is_employee_or_super)
def product_delete(request, sku):
    product = get_object_or_404(Product, sku=sku)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "store/product_confirm_delete.html", {"product": product})


@login_required
def product_detail(request, sku):
    product = get_object_or_404(Product, sku=sku)
    reviews = product.reviews.select_related("client__user").order_by("-date")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.client = request.user.client_profile
            review.save()
            return redirect("product_detail", sku=sku)
    else:
        form = ReviewForm()

    return render(request, "store/product_detail.html", {
        "product": product,
        "reviews": reviews,
        "form": form,
    })


@login_required
@employee_required
def employee_dashboard(request):
    emp = request.user.employee_profile
    sales = (Sale.objects
                  .filter(employee=emp)
                  .select_related("product", "client")
                  .order_by("-date"))

    # статистика по поставщикам
    supplier_stats = []
    for sup in Supplier.objects.all():
        sup_sales = [s for s in sales if sup in s.product.suppliers.all()]
        if not sup_sales:
            continue
        supplier_stats.append({
            "supplier":    sup,
            "sales_count": len(sup_sales),
            "revenue":     sum(s.price for s in sup_sales),
        })

    # группировка по дате
    daily = (sales
             .annotate(day=TruncDate("date"))
             .values("day")
             .annotate(count=Count("id"))
             .order_by("day"))
    dates  = [entry["day"] for entry in daily]
    counts = [entry["count"] for entry in daily]

    # строим график
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(dates, counts, marker="o")
    ax.set_title("Продажи по дням")
    ax.set_xlabel("Дата")
    ax.set_ylabel("Число продаж")
    ax.grid(True)
    fig.autofmt_xdate()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    chart_png = base64.b64encode(buf.getvalue()).decode("ascii")
    buf.close()

    return render(request, "store/employee_dashboard.html", {
        "sales":          sales,
        "supplier_stats": supplier_stats,
        "emp":            emp,
        "chart_png":      chart_png,
    })


@login_required
def create_sale(request, sku):
    product = get_object_or_404(Product, sku=sku)
    if request.method == "POST":
        form = SaleForm(request.POST, user=request.user)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.product = product
            if hasattr(request.user, "employee_profile"):
                sale.employee = request.user.employee_profile
            else:
                sale.client = request.user.client_profile
            sale.price = sale.quantity * product.price
            sale.save()
            return redirect("employee_dashboard" if hasattr(request.user, "employee_profile") else "profile")
    else:
        form = SaleForm(user=request.user)

    return render(request, "store/sale_create.html", {
        "product": product,
        "form": form,
    })


@login_required
def order_list(request):
    sales = (request.user.client_profile.sales
             .select_related("product")
             .order_by("-date"))
    return render(request, "store/order_list.html", {"sales": sales})


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(
        request.user.client_profile.sales.select_related("product"),
        pk=pk
    )
    return render(request, "store/sale_detail.html", {"sale": sale})


@login_required
def cancel_sale(request, pk):
    sale = get_object_or_404(request.user.client_profile.sales, pk=pk)
    if request.method == "POST":
        sale.delete()
        messages.info(request, f"Заказ #{pk} отменён.")
        return redirect("order_list")
    return render(request, "store/sale_cancel.html", {"sale": sale})


@login_required
def profile(request):
    client = request.user.client_profile
    orders = Sale.objects.filter(client=client).select_related("product").order_by("-date")
    return render(request, "store/profile.html", {
        "client": client,
        "sales":  orders,
    })


@login_required
def profile_edit(request):
    client = request.user.client_profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=client, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён")
            return redirect("profile")
    else:
        form = ProfileForm(instance=client, user=request.user)

    return render(request, "store/profile_edit.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def product_list(request):
    categories = Category.objects.all()
    suppliers  = Supplier.objects.all()

    q          = request.GET.get("q", "").strip()
    sku        = request.GET.get("sku", "").strip()
    category   = request.GET.get("category", "")
    supplier   = request.GET.get("supplier", "")
    min_price  = request.GET.get("min_price", "")
    max_price  = request.GET.get("max_price", "")
    sort       = request.GET.get("sort", "")

    products = (Product.objects
                .select_related("category")
                .prefetch_related("suppliers")
                .all())

    if q:
        products = products.filter(name__icontains=q)
    if sku:
        products = products.filter(sku__icontains=sku)
    if category:
        products = products.filter(category_id=category)
    if supplier:
        products = products.filter(suppliers__id=supplier)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if sort in ("name", "-name", "price", "-price"):
        products = products.order_by(sort)

    paginator   = Paginator(products, 5)
    page_number = request.GET.get("page")
    page_obj    = paginator.get_page(page_number)

    return render(request, "store/product_list.html", {
        "page_obj":           page_obj,
        "categories":         categories,
        "suppliers":          suppliers,
        "selected_q":         q,
        "selected_sku":       sku,
        "selected_category":  category,
        "selected_supplier":  supplier,
        "selected_min_price": min_price,
        "selected_max_price": max_price,
        "selected_sort":      sort,
    })


@require_GET
def products_data(request):
    """Возвращает JSON со списком продуктов (без серверной пагинации),
    поддерживает те же фильтры, что и `product_list`.
    """
    q = request.GET.get("q", "").strip()
    sku = request.GET.get("sku", "").strip()
    category = request.GET.get("category", "")
    supplier = request.GET.get("supplier", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    sort = request.GET.get("sort", "")

    products = (Product.objects
                .select_related("category")
                .prefetch_related("suppliers")
                .all())

    if q:
        products = products.filter(name__icontains=q)
    if sku:
        products = products.filter(sku__icontains=sku)
    if category:
        products = products.filter(category_id=category)
    if supplier:
        products = products.filter(suppliers__id=supplier)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if sort in ("name", "-name", "price", "-price"):
        products = products.order_by(sort)

    result = []
    for p in products:
        result.append({
            'sku': p.sku,
            'name': p.name,
            'price': str(p.price),
            'category__name': p.category.name if p.category else '',
        })

    return JsonResponse({'products': result})


# def news(request):
#     page      = int(request.GET.get("page", 1))
#     page_size = 5
#     articles  = fetch_news(page_size=page_size, page=page)
#     has_more  = len(articles) == page_size
#     #rates     = fetch_exchange_rates(base="BYN", symbols=["USD", "EUR"])
#     rates = fetch_nbrb_rates(symbols=["USD", "EUR"])


#     return render(request, "store/news.html", {
#         "articles": articles,
#         "rates":     rates,
#         "page":      page,
#         "has_more":  has_more,
#     })


@login_required
def exchange_api(request):
    symbols_param = request.GET.get("symbols")
    symbols = symbols_param.split(",") if symbols_param else None
    rates = fetch_exchange_rates(base="BYN", symbols=symbols)
    return JsonResponse({
        "base": "BYN",
        "rates": rates
    })


from django.views.decorators.http import require_POST
from .models import Product

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(sku__in=cart.keys())
    cart_items = []
    for product in products:
        quantity = cart[str(product.sku)]
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': product.price * quantity
        })
    total_price = sum(item['total'] for item in cart_items)
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@require_POST
def cart_add(request, sku):
    cart = request.session.get('cart', {})
    cart[sku] = cart.get(sku, 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

@require_POST
def cart_remove(request, sku):
    cart = request.session.get('cart', {})
    if sku in cart:
        del cart[sku]
    request.session['cart'] = cart
    return redirect('cart')

@require_POST
def cart_update(request, sku):
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    if quantity > 0:
        cart[sku] = quantity
    else:
        cart.pop(sku, None)
    request.session['cart'] = cart
    return redirect('cart')

from django.contrib.auth.decorators import login_required
from .models import Product, Sale

@login_required
def cart_checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Корзина пуста.")
        return redirect('cart')
    client = request.user.client_profile
    for sku, quantity in cart.items():
        product = Product.objects.get(sku=sku)
        Sale.objects.create(
            product=product,
            client=client,
            quantity=quantity,
            price=product.price * quantity
        )
    request.session['cart'] = {}  # очистить корзину
    messages.success(request, "Заказ успешно оформлен!")
    return redirect('profile')
