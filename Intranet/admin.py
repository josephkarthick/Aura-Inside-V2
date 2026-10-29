from django.contrib import admin
from .models import BoardMembers, Home, GalleryGroup, Gallery, FloatingFlag, Quote

@admin.register(BoardMembers)
class BoardMembersAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'manager')  # Columns shown in list view
    search_fields = ('name', 'role')            # Adds a search box
    list_filter = ('role',)                     # Filters by role
    autocomplete_fields = ['manager']           # Dropdown search for manager selection

    fieldsets = (
        (None, {
            'fields': ('id', 'name', 'role', 'photo_url', 'manager')
        }),
    )

@admin.register(GalleryGroup)
class GalleryGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("title", "group", "image_preview", "likes", "created_at")
    list_filter = ("group", "created_at")
    search_fields = ("title", "description", "group__name")
    readonly_fields = ("image_preview",)
    ordering = ("-created_at",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px;">', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"

@admin.register(FloatingFlag)
class FloatingFlagAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "updated_at")
    list_editable = ("is_active",)
    


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "is_active")
    list_filter = ("is_active",)
    search_fields = ("text", "author")    
    