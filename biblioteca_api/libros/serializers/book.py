from rest_framework import serializers
from ..models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'isbn', 'titulo', 'autor', 'editorial', 'anio_publicacion',
            'categoria', 'num_paginas', 'ubicacion', 'estado', 'copias_disponibles'
        ]