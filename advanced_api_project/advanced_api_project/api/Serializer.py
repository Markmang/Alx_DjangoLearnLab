from rest_framework import serializers
from .models import Author, Book
import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    - Serializes all fields of the Book model.
    - Includes custom validation to ensure publication_year is not in the future.
    """

    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']  # serialize all fields in the Book model

    def validate_publication_year(self, value):
        """
        Custom validation method to check if the publication year
        is not greater than the current year.
        """
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    - Serializes the `name` field.
    - Includes a nested BookSerializer to dynamically show the related books.
    """
    books = BookSerializer(many=True, read_only=True)  
    # `many=True` means one author can have many books.
    # `read_only=True` means books are only shown when retrieving data, 
    # not when creating/updating an author.

    class Meta:
        model = Author
        fields = ['name', 'books']  # only include name and nested books
