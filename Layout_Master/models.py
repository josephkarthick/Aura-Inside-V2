from django.db import models
from Accounts.models import Department, Designation, AuraInsideUser

VISIBILITY_CHOICES = [
    ('public', 'Public (No Login Required)'),
    ('authenticated', 'Login Required'),
    ('department', 'Department Based'),
]


class Menu(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    departments = models.ManyToManyField(Department, blank=True)
    # Legacy designation relation retained for compatibility.
    designations = models.ManyToManyField(Designation, blank=True, related_name='layout_menus')
    users = models.ManyToManyField(AuraInsideUser, blank=True, related_name='layout_menus')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')

    def __str__(self):
        return self.name


class SubMenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='submenus')
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    departments = models.ManyToManyField(Department, blank=True)
    # Legacy designation relation retained for compatibility.
    designations = models.ManyToManyField(Designation, blank=True, related_name='layout_submenus')
    users = models.ManyToManyField(AuraInsideUser, blank=True, related_name='layout_submenus')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')

    def __str__(self):
        return f'{self.menu.name} → {self.name}'


class ChildMenu(models.Model):
    submenu = models.ForeignKey(SubMenu, on_delete=models.CASCADE, related_name='child_menus')
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255, blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    departments = models.ManyToManyField(Department, blank=True)
    # Legacy designation relation retained for compatibility.
    designations = models.ManyToManyField(Designation, blank=True, related_name='layout_childmenus')
    users = models.ManyToManyField(AuraInsideUser, blank=True, related_name='layout_childmenus')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')

    def __str__(self):
        return f'{self.submenu.menu.name} → {self.submenu.name} → {self.name}'


class MenuDesignationAccess(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='designation_rules')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['menu', 'department', 'designation'], name='uniq_menu_dept_designation_access')]

    def __str__(self):
        return f'{self.menu} — {self.department} — {self.designation}'


class SubMenuDesignationAccess(models.Model):
    submenu = models.ForeignKey(SubMenu, on_delete=models.CASCADE, related_name='designation_rules')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['submenu', 'department', 'designation'], name='uniq_submenu_dept_designation_access')]

    def __str__(self):
        return f'{self.submenu} — {self.department} — {self.designation}'


class ChildMenuDesignationAccess(models.Model):
    childmenu = models.ForeignKey(ChildMenu, on_delete=models.CASCADE, related_name='designation_rules')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['childmenu', 'department', 'designation'], name='uniq_childmenu_dept_designation_access')]

    def __str__(self):
        return f'{self.childmenu} — {self.department} — {self.designation}'
