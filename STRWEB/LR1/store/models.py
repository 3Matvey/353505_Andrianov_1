from django.db import models
from django.contrib.auth.models import User
from .validators import validate_age_18


class Partner(models.Model):
    name = models.CharField("Название", max_length=200)
    website = models.URLField("Сайт", blank=True)
    logo = models.ImageField("Логотип", upload_to="partners/", blank=True, null=True)

    class Meta:
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    code = models.CharField("Код", max_length=50, unique=True)
    discount = models.PositiveIntegerField("Скидка в %")
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        ordering = ["-created_at"]

    def __str__(self):
        return self.code


class CompanyNews(models.Model):
    title        = models.CharField("Заголовок", max_length=255)
    content      = models.TextField("Содержание")
    image        = models.ImageField("Картинка", upload_to="news/", blank=True, null=True)
    published_at = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = "Новость компании"
        verbose_name_plural = "Новости компании"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title



class CompanyInfo(models.Model):
    """
    Раздел «О компании» — сюда вы будете складывать любые 
    текстовые блоки (историю по годам, реквизиты, логотипы, видео…).
    """
    title   = models.CharField("Заголовок", max_length=100)
    content = models.TextField("Текст")
    order   = models.PositiveIntegerField("Порядок вывода", default=0)

    class Meta:
        verbose_name = "Блок компании"
        verbose_name_plural = "О компании"
        ordering = ['order']

    def __str__(self):
        return self.title


class FAQ(models.Model):
    """
    Раздел «Словарь терминов и понятий» (часто задаваемые вопросы).
    """
    question   = models.CharField("Вопрос", max_length=255)
    answer     = models.TextField("Ответ")
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Вопрос/ответ"
        verbose_name_plural = "Словарь (FAQ)"
        ordering = ['-created_at']

    def __str__(self):
        return self.question
    

class Contact(models.Model):
    """
    Раздел «Контакты»: фото сотрудников, их роль, телефоны, почта, описание.
    """
    name        = models.CharField("Имя", max_length=100)
    role        = models.CharField("Должность / роль", max_length=100)
    photo       = models.ImageField("Фото", upload_to='contacts/', blank=True, null=True)
    phone       = models.CharField("Телефон", max_length=30, blank=True)
    email       = models.EmailField("Email", blank=True)
    description = models.TextField("Краткое описание", blank=True)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"{self.name} — {self.role}"


class Vacancy(models.Model):
    """
    Раздел «Вакансии»: список открытых вакансий.
    """
    title      = models.CharField("Название вакансии", max_length=200)
    description= models.TextField("Описание вакансии")
    posted_at  = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-posted_at']

    def __str__(self):
        return self.title
    
class Review(models.Model):
    RATING_CHOICES = [(i, f"{i} ⭐") for i in range(1, 6)]

    product  = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    client   = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating   = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )
    comment  = models.TextField()
    date     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.product.name} — {self.client.user.username} ({self.rating}★)"

class Supplier(models.Model):
    name    = models.CharField("Название поставщика", max_length=200)
    address = models.CharField("Адрес", max_length=300, blank=True)
    phone   = models.CharField("Телефон", max_length=30, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField("Категория", max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    sku        = models.CharField("Артикул", max_length=50, unique=True)
    name       = models.CharField("Название товара", max_length=200)
    price      = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    category   = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    suppliers  = models.ManyToManyField(Supplier, related_name="products", blank=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

class Client(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    phone      = models.CharField('Телефон', max_length=30)
    birth_date = models.DateField('Дата рождения', null=True, blank=True, validators=[validate_age_18])
    def __str__(self):
        return self.user.username

class Employee(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    position   = models.CharField('Должность', max_length=100)
    phone      = models.CharField('Телефон', max_length=30)
    birth_date = models.DateField('Дата рождения',  null=True, blank=True, validators=[validate_age_18])
    def __str__(self):
        return f"{self.position} — {self.user.username}"

class Sale(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales")
    client     = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales")
    employee   = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales")
    date       = models.DateTimeField("Дата продажи", auto_now_add=True)
    quantity   = models.PositiveIntegerField("Количество", default=1)
    price      = models.DecimalField("Итоговая цена", max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Sale #{self.pk} – {self.product.name} x{self.quantity}"
