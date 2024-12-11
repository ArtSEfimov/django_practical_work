from django.urls import path
from book import views

urlpatterns = [
    # path('', views.books_list, name='books_list'),
    # path('<int:pk>', views.book_detail, name='books_detail'),
    path('', views.BookListView.as_view(), name='books_list'),
    path('<int:pk>', views.BookDetailView.as_view(), name='books_detail')
]
