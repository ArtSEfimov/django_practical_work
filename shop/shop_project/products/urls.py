from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='index'),  # http://127.0.0.1:8000/products/
    path('page/<int:page>/', views.ProductsListView.as_view(), name='paginator'),

    path('category/<int:category_id>/', views.ProductsListView.as_view(), name='category'),
    path('category/<int:category_id>/page/<int:page>/', views.ProductsListView.as_view(),
         name='category_paginator'),

    path('baskets/add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
]
