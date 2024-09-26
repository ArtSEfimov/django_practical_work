from django.core.paginator import Paginator
from django.shortcuts import render

from products.models import Product, ProductCategory

# FBV for products_app

def index(request):
    context = {
        'title': 'Store',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page_number=1):
    if category_id:
        products_by_category = Product.objects.filter(category__id=category_id)
    else:
        products_by_category = Product.objects.all()

    per_page = 3
    paginator = Paginator(products_by_category, per_page)
    products_paginator = paginator.page(page_number)

    context = {
        'title': 'Store - Каталог',
        'products': products_paginator,
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'products/products.html', context)
