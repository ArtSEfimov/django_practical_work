from django.http import Http404
from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from book.models import Book
from book.serializers import BookSerializer


# class BookListView(APIView):
#     def get(self, request):
#         books = Book.objects.all()
#         serializer_books = BookSerializer(books, many=True)
#         return Response(serializer_books.data)
#
#     def post(self, request):
#         serializer_book = BookSerializer(data=request.data)
#         if serializer_book.is_valid():
#             serializer_book.save()
#             return Response(serializer_book.data, status=201)
#         return Response(serializer_book.errors, status=400)
#
#
# class BookDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         book = self.get_object(pk)
#         serializer_book = BookSerializer(book)
#         return Response(serializer_book.data)
#
#     def put(self, request, pk):
#         book = self.get_object(pk)
#         serializer_book = BookSerializer(book, data=request.data)
#         if serializer_book.is_valid():
#             serializer_book.save()
#             return Response(serializer_book.data)
#         return Response(serializer_book.errors, status=400)
#
#     def delete(self, request, pk):
#         book = self.get_object(pk)
#         book.delete()
#         return Response(status=204)


class BookListView(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'

    @action(detail=True, methods=['get'])
    def authors(self, request, pk=None):
        book = self.get_object()
        return Response({'author': book.author})
