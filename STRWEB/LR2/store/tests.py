from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Supplier, Product, Client, Employee, Sale

class StoreSmokeTests(TestCase):
    def setUp(self):
        # создаём пользователей
        self.user = User.objects.create_user('joe', 'joe@example.com', 'pass1234')
        self.client_profile = Client.objects.create(
            user=self.user, phone='+70001112233', birth_date='2000-01-01'
        )
        self.employee_user = User.objects.create_user('kate', 'kate@example.com', 'pass1234')
        self.emp = Employee.objects.create(user=self.employee_user, position='Manager')
        # пара категорий/товаров
        cat = Category.objects.create(name='Корм')
        sup = Supplier.objects.create(name='Ферма', phone='123', address='Поле')
        self.prod = Product.objects.create(sku='FOODX', name='КормX', price=100, category=cat)
        self.prod.suppliers.add(sup)

    def test_product_list_basic(self):
        resp = self.client.get(reverse('product_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Список товаров')

    def test_product_detail(self):
        resp = self.client.get(reverse('product_detail', args=[self.prod.sku]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'КормX')
        self.assertContains(resp, 'Ферма')

    def test_signup_creates_client(self):
        resp = self.client.post(reverse('signup'), {
            'username': 'alex', 'email': 'a@b.c',
            'date_of_birth': '1990-05-05',
            'phone': '+79998887766',
            'password1': 'passw0rd!', 'password2': 'passw0rd!'
        })
        self.assertEqual(resp.status_code, 302)
        u = User.objects.get(username='alex')
        self.assertTrue(hasattr(u, 'client_profile'))
        self.assertEqual(u.client_profile.phone, '+79998887766')

    def test_employee_dashboard_requires_employee(self):
        # без логина → редирект на логин
        resp = self.client.get(reverse('employee_dashboard'))
        self.assertEqual(resp.status_code, 302)

        # клиент вошёл → 403
        self.client.login(username='joe', password='pass1234')
        resp = self.client.get(reverse('employee_dashboard'))
        self.assertEqual(resp.status_code, 403)

        # сотрудник вошёл → 200 и содержимое
        self.client.login(username='kate', password='pass1234')
        resp = self.client.get(reverse('employee_dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Дашборд')

    def test_product_delete_requires_employee(self):
        url = reverse('product_delete', args=[self.prod.sku])

        # 1) без логина → редирект на логин
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

        # 2) обычный клиент → 403 Forbidden
        self.client.login(username='joe', password='pass1234')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

        # 3) сотрудник → 200 (страница подтверждения)
        self.client.login(username='kate', password='pass1234')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Удалить товар')

        # 4) POST удаляет и редиректит обратно в список
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('product_list'))
        # товара уже нет в БД
        self.assertFalse(Product.objects.filter(pk=self.prod.pk).exists())
