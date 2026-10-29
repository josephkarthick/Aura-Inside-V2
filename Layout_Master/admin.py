from django.contrib import admin
from .models import Menu, SubMenu, ChildMenu
from django.utils.html import format_html


# Optional: display visibility with a colored badge in admin list
def visibility_status(obj):
    color_map = {
        'public': 'green',
        'authenticated': 'orange',
        'department': 'blue',
    }
    color = color_map.get(obj.visibility, 'gray')
    return format_html(
        '<span style="color: {};">{}</span>',
        color, obj.get_visibility_display()
    )
visibility_status.short_description = 'Visibility'

class ChildMenuInline(admin.TabularInline):
    model = ChildMenu
    extra = 1

class SubMenuInline(admin.TabularInline):
    model = SubMenu
    extra = 1

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "order", visibility_status)
    ordering = ("order",)
    inlines = [SubMenuInline]
    filter_horizontal = ("departments",)

@admin.register(SubMenu)
class SubMenuAdmin(admin.ModelAdmin):
    list_display = ("name", "menu", "order", visibility_status)
    ordering = ("menu", "order")
    inlines = [ChildMenuInline]
    filter_horizontal = ("departments",)

@admin.register(ChildMenu)
class ChildMenuAdmin(admin.ModelAdmin):
    list_display = ("name", "submenu", "url", "order", visibility_status)
    ordering = ("submenu", "order")
    filter_horizontal = ("departments",)
