from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        """
        Setup runs before every test. 
        Create test users, author, and some book data.
        """
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.author = Author.objects.create(name="John Doe")
        self.book = Book.objects.create(
            title="Sample Book",
            publication_year=2020,
            author=self.author
        )
        # Endpoints
        self.list_url = reverse("book-list")  # /books/
        self.detail_url = reverse("book-detail", kwargs={"pk": self.book.id})  # /books/<id>/

    def test_list_books(self):
        """Test GET request to list all books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_book_authenticated(self):
        """Test authenticated user can create a book"""
        self.client.login(username="testuser", password="password123")
        data = {"title": "New Book", "publication_year": 2022, "author": self.author.id}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        """Test unauthenticated users cannot create a book"""
        data = {"title": "Unauthorized Book", "publication_year": 2022, "author": self.author.id}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        """Test authenticated user can update a book"""
        self.client.login(username="testuser", password="password123")
        data = {"title": "Updated Title", "publication_year": 2021, "author": self.author.id}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book(self):
        """Test authenticated user can delete a book"""
        self.client.login(username="testuser", password="password123")
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_year(self):
        """Test filtering books by publication_year"""
        response = self.client.get(self.list_url, {"publication_year": 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Sample Book")

    def test_search_books(self):
        """Test searching books by title"""
        response = self.client.get(self.list_url, {"search": "Sample"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Sample Book")

    def test_order_books(self):
        """Test ordering books by publication_year"""
        Book.objects.create(title="Older Book", publication_year=2010, author=self.author)
        response = self.client.get(self.list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Older Book")
