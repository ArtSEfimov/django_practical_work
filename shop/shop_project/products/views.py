from django.shortcuts import render
from django.views.generic import ListView
from .models import Product, ProductCategory, Basket
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView


# Create your views here.

# CBV

class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Store'})
        return context


# FBV

# def index(request):
#     context = {
#         'title': 'Store',
#     }
#     return render(request, 'products/index.html', context)

class CommonListView:
    model = Product
    template_name = 'products/products.html'

    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update(
            {
                'title': 'Store - Каталог',
                'categories': ProductCategory.objects.all()
            }
        )
        return context


class ProductsListView(CommonListView, ListView):

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            return queryset.filter(category__id=category_id)
        return queryset


class CategoriesListView(CommonListView, ListView):

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            return queryset.filter(category__id=category_id)
        return queryset


#
# def products(request, category_id=None, page_number=1):
#     if category_id:
#         products_by_category = Product.objects.filter(category__id=category_id)
#     else:
#         products_by_category = Product.objects.all()
#
#     per_page = 3
#     paginator = Paginator(products_by_category, per_page)
#     products_paginator = paginator.page(page_number)
#
#     context = {
#         'title': 'Store - Каталог',
#         'products': products_paginator,
#         'categories': ProductCategory.objects.all()
#     }
#     return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(pk=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity = F('quantity') + 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
