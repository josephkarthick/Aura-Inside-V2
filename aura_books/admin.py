from django.contrib import admin
from .models import Book, BookPage

class BookPageInline(admin.StackedInline): # Changed to Stacked for better readability
    model = BookPage
    extra = 1
    ordering = ["page_order"]
    
    # Grouping page content for a cleaner look
    fieldsets = (
        (None, {
            'fields': ('page_order',)
        }),
        ('Text Content', {
            'fields': ('heading', 'paragraph')
        }),
    )

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year", "created_at")
    list_filter = ("year", "author")
    search_fields = ("title", "author")
    
    inlines = [BookPageInline]

    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "author", "year")
        }),
        ("Front Cover & Inside", {
            "fields": (
                "front_cover_image", 
                "front_inside_cover_image", 
                "front_inside_cover_text"
            )
        }),
        ("Back Cover & Inside", {
            "fields": (
                "back_cover_image", 
                "back_inside_cover_image", 
                "back_inside_cover_text"
            )
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ("created_at",)