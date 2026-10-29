from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AuraInsideUser, Department, Designation,Shift
import csv
from django.http import HttpResponse

def export_as_csv(modeladmin, request, queryset):
    model = modeladmin.model
    meta = model._meta

    # Get ALL concrete DB fields automatically
    field_names = [field.name for field in meta.concrete_fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        f'attachment; filename={meta.model_name}.csv'
    )

    writer = csv.writer(response)
    writer.writerow(field_names)

    for obj in queryset:
        row = []
        for field in field_names:
            value = getattr(obj, field)
            # Handle ForeignKey display safely
            row.append(str(value) if value is not None else '')
        writer.writerow(row)

    return response

export_as_csv.short_description = "Export selected users (ALL columns)"


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AuraInsideUser

@admin.register(AuraInsideUser)
class AuraInsideUserAdmin(UserAdmin):
    model = AuraInsideUser
    actions = [export_as_csv]

    list_display = [
        'username', 'email', 'employee_id',
        'department', 'designation', 'shift',
        'is_active', 'is_staff'
    ]
    list_filter = [
        'is_staff', 'is_superuser', 'is_active',
        'gender', 'department', 'designation', 'shift'
    ]
    search_fields = ['username', 'email', 'employee_id']
    ordering = ['username']

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'employee_id', 'department', 'designation',
                'gender', 'birthdate', 'shift',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'classes': ('wide',),
            'fields': (
                'employee_id', 'department', 'designation',
                'gender', 'birthdate', 'shift',
            )
        }),
    )




@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'timezone')
