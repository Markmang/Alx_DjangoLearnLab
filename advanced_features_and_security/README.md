# Permissions & Groups Setup

This project demonstrates Django's groups and permissions system.

## Custom Permissions
Defined in `bookshelf/models.py` inside the `Book` model:
- `can_view` – View books
- `can_create` – Create books
- `can_edit` – Edit books
- `can_delete` – Delete books

## Groups
Configured via Django Admin:
- **Viewers**: `can_view`
- **Editors**: `can_view`, `can_create`, `can_edit`
- **Admins**: All permissions

## Views
Permission checks are enforced using `@permission_required` in `bookshelf/views.py`.

Example:
```python
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, book_id):
    ...
