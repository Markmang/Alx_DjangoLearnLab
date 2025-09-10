# CRUD Operations with Django ORM

# CRUD Operations with Django ORM

This file documents Create, Retrieve, Update, and Delete operations performed on the `Book` model in the Django shell.

---

```python
from bookshelf.models import Book

# -------------------------
# 1. CREATE
# -------------------------
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# <Book: 1984 by George Orwell (1949)>

# -------------------------
# 2. RETRIEVE
# -------------------------
retrieved_book = Book.objects.get(id=book.id)
retrieved_book.title, retrieved_book.author, retrieved_book.publication_year
# ('1984', 'George Orwell', 1949)

# -------------------------
# 3. UPDATE
# -------------------------
book = Book.objects.get(id=book.id)
book.title = "Nineteen Eighty-Four"
book.save()
Book.objects.get(id=book.id).title
# 'Nineteen Eighty-Four'

# -------------------------
# 4. DELETE
# -------------------------
book = Book.objects.get(id=book.id)
book.delete()
Book.objects.all()
# <QuerySet []>
