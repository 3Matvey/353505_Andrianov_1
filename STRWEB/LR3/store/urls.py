# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),

    # Новости компании (CRUD)
    path('news/', views.news, name='news'),
    path('news/add/', views.news_create, name='news-create'),
    path('news/<int:pk>/', views.news_detail, name='news-detail'),
    path('news/<int:pk>/edit/', views.news_update, name='news-update'),
    path('news/<int:pk>/delete/', views.news_delete, name='news-delete'),

    # Продукты
    path('products/', views.product_list, name='product_list'),
    path('products/data/', views.products_data, name='products_data'),
    path('products/<str:sku>/', views.product_detail, name='product_detail'),
    path('products/<str:sku>/buy/', views.create_sale, name='product_buy'),
    path('products/<str:sku>/delete/', views.product_delete, name='product_delete'),

    # Заказы (продажи)
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('orders/<int:pk>/cancel/', views.cancel_sale, name='sale_cancel'),

    # Профиль пользователя
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # Панель сотрудника
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/sale/add/<str:sku>/', views.create_sale, name='employee_create_sale'),

    # API обмена валют
    path('api/exchange/', views.exchange_api, name='exchange_api'),

    # Статические страницы сайта
    path('about/', views.about, name='about'),
    path('glossary/', views.glossary, name='glossary'),
    path('contacts/', views.contacts, name='contacts'),
    path('contacts/lab/', views.contacts_lab, name='contacts_lab'),
    path('contacts/lab/data/', views.contacts_lab_data, name='contacts_lab_data'),
    path('contacts/lab/add/', views.contacts_lab_add, name='contacts_lab_add'),
    path('privacy/', views.privacy, name='privacy'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('promocodes/', views.promocodes, name='promocodes'),
    path('slider/', views.slider_page, name='slider'),
    path('students/', views.students, name='students'),
    path('chart/', views.chart_page, name='chart'),
    path('scroll-anim/', views.scroll_anim, name='scroll_anim'),

    # Корзина
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<str:sku>/', views.cart_add, name='cart_add'),
    path('cart/remove/<str:sku>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<str:sku>/', views.cart_update, name='cart_update'),
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),
]
