from django.contrib import admin
from .models import CompanyNews, Supplier, Category, Product, Client, Employee, Sale, Review, CompanyInfo, FAQ, Contact, Vacancy, Partner, PromoCode

@admin.register(CompanyNews)
class CompanyNewsAdmin(admin.ModelAdmin):
    list_display   = ("title", "published_at")
    readonly_fields = ("published_at",)
    search_fields  = ("title",)
    list_per_page  = 20


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('order','title')
    ordering     = ('order',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question','created_at')
    readonly_fields = ('created_at',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','role','phone','email')
    search_fields = ('name','role','email')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title','posted_at')
    readonly_fields = ('posted_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('product', 'client', 'rating', 'date')
    list_filter   = ('rating', 'date')
    search_fields = ('client__user__username', 'product__name', 'comment')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'address')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('sku', 'name', 'price', 'category')
    list_filter   = ('category', 'suppliers')
    search_fields = ('sku', 'name')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth_date')
    search_fields = ('user__username', 'user__email')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'birth_date')
    search_fields = ('user__username', 'position')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display    = ('id', 'product', 'client', 'employee', 'date', 'quantity', 'price')
    list_filter     = ('date', 'product')
    date_hierarchy  = 'date'

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "website")


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount", "is_active")
    list_filter  = ("is_active",)