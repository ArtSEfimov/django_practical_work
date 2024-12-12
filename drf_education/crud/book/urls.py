from django.urls import path, include
from rest_framework import routers

from book import views
from book.views import BookListView

router = routers.DefaultRouter()
router.register('api', BookListView)

urlpatterns = [
    # path('', views.books_list, name='books_list'),
    # path('<int:pk>', views.book_detail, name='books_detail'),
    #     path('', views.BookListView.as_view(), name='books_list'),
    #     path('<int:pk>', views.BookDetailView.as_view(), name='books_detail')
    path('', include(router.urls))
]
