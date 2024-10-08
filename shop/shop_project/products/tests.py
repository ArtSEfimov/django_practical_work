from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Product, ProductCategory

# Create your tests here.

class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'fixtures/categories.json',
        'fixtures/products.json',
    ]

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_test(response)
        self.assertQuerySetEqual(self.products[:3], response.context_data['object_list'], ordered=False)

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_test(response)
        self.assertQuerySetEqual(
            response.context_data['object_list'],
            self.products.filter(category__id=category.id)[:3],
            ordered=False
        )

    def _common_test(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
