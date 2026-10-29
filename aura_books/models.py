from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=150, null=True)
    year = models.PositiveIntegerField(null=True)

    front_cover_image = models.ImageField(upload_to="books/covers/", null=True)
    front_inside_cover_image = models.ImageField(
        upload_to="books/covers/", blank=True, null=True
    )
    front_inside_cover_text = models.TextField(blank=True, null=True)

    back_cover_image = models.ImageField(upload_to="books/covers/", null=True)
    back_inside_cover_image = models.ImageField(
        upload_to="books/covers/", blank=True, null=True
    )
    back_inside_cover_text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title or "Untitled Book"


class BookPage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="pages")
    page_order = models.PositiveIntegerField()

    heading = models.CharField(max_length=150, blank=True)
    paragraph = models.TextField(blank=True)  # rich HTML content

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["page_order"]

    def __str__(self):
        return f"{self.book.title} – Page {self.page_order}"



