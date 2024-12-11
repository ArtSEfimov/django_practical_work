from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from book.models import Book
from book.serializers import BookSerializer


# Create your views here.


@api_view(["get", "post"])
def books_list(request):
    if request.method == 'GET':
        items = Book.objects.all()
        serializer_books = BookSerializer(items, many=True)
        return Response(serializer_books.data)
    if request.method == 'POST':
        serializer_books = BookSerializer(data=request.data)
        if serializer_books.is_valid():
            serializer_books.save()
            return Response(serializer_books.data, status=201)
        return Response(serializer_books.errors, status=400)


@api_view(['get', 'put', 'delete'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer_book = BookSerializer(book)
        return Response(serializer_book.data)
    elif request.method == 'PUT':
        serializer_book = BookSerializer(book, data=request.data)
        if serializer_book.is_valid():
            serializer_book.save()
            return Response(serializer_book.data)
        return Response(serializer_book.errors, status=400)
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=204)
