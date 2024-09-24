from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>', views.ProductsListView.as_view(), name='category'),
    path('page/<int:page>', views.ProductsListView.as_view(), name='paginator'),
    path('category/<int:category_id>/page/<int:page>', views.ProductsListView.as_view(), name='paginate_by_category'),


    path('baskets/add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
]
