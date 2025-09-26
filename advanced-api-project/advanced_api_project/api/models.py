from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)

    def _str_(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def _str_(self):
        return f"{self.title} ({self.publication_year})"
