# Update Operation

```python
from bookshelf.models import Book

# Update the book title
book = Book.objects.get(id=book.id)
book.title = "Nineteen Eighty-Four"
book.save()

# Verify update
Book.objects.get(id=book.id).title
# 'Nineteen Eighty-Four'
