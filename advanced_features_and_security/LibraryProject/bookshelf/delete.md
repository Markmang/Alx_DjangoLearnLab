# Delete Operation

```python
from bookshelf.models import Book

# Delete the book
book = Book.objects.get(id=book.id)
book.delete()

# Confirm deletion
Book.objects.all()
# <QuerySet []>
