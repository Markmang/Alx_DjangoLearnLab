from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend


# List all books (read-only for unauthenticated users, full access for logged-in users)
class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Advanced filtering, searching, ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # For DjangoFilterBackend
    filterset_fields = ['title', 'author', 'publication_year']

    # For SearchFilter (text lookup)
    search_fields = ['title', 'author__name']

    # For OrderingFilter
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering

    def get_queryset(self):
        """
        This view can return a filtered list of books.
        Supports:
        - Filtering against query params (?author=, ?publication_year=)
        - Restricting to authenticated user's books (if needed)
        - Searching & ordering (via DRF backends)
        """
        queryset = Book.objects.all()

        # Example: restrict to current user’s books (if Book has an owner field)
        if self.request.user.is_authenticated:
            user_only = self.request.query_params.get('mine')
            if user_only == 'true':
                queryset = queryset.filter(owner=self.request.user)

        # Example: filter against query param manually
        title_param = self.request.query_params.get('title')
        if title_param:
            queryset = queryset.filter(title__icontains=title_param)

        return queryset

# Retrieve a single book by ID (same read-only rule)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Create a new book (only for authenticated users)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    # Automatically link logged-in user as the author (if your User → Author relation exists)
    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)


# Update a book (only for authenticated users)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# Delete a book (only for authenticated users)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
