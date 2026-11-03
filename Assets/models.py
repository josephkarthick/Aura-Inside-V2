
from django.db import models
from django.conf import settings


# ============================================================
# ASSET CATEGORY
# ============================================================

class AssetCategory(models.Model):

    CATEGORY_TYPES = [
        ('IT', 'IT Assets'),
        ('NON_IT', 'Non-IT Assets'),
    ]

    name = models.CharField(max_length=100)

    category_type = models.CharField(
        max_length=10,
        choices=CATEGORY_TYPES
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category_type', 'name']
        verbose_name_plural = 'Asset Categories'

    def __str__(self):
        return self.name


# ============================================================
# ASSET MASTER
# ============================================================

class Asset(models.Model):

    STATUS_CHOICES = [
        ('IN_STOCK', 'In Stock'),
        ('IN_USE', 'In Use'),
        ('SHARED', 'Shared'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('DAMAGED', 'Damaged'),
        ('DISPOSED', 'Disposed'),
        ('EXPIRED', 'Expired'),
    ]

    asset_tag = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    asset_name = models.CharField(max_length=200)

    category = models.ForeignKey(
        AssetCategory,
        on_delete=models.PROTECT,
        related_name='assets'
    )

    manufacturer = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    model = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    serial_number = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    purchase_date = models.DateField(
        blank=True,
        null=True
    )

    purchase_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    warranty_start = models.DateField(
        blank=True,
        null=True
    )

    warranty_end = models.DateField(
        blank=True,
        null=True
    )

    assigned_employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='assigned_assets'
    )

    department = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='IN_STOCK'
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.asset_tag or 'Unassigned'} - {self.asset_name}"





# ============================================================
# ASSET ASSIGNMENT HISTORY
# ============================================================

class AssetAssignment(models.Model):

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='assignment_history'
    )

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='asset_assignment_history'
    )

    assigned_date = models.DateField()

    returned_date = models.DateField(
        blank=True,
        null=True
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='assets_assigned_by'
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-assigned_date']

    def __str__(self):
        return f"{self.asset} - {self.employee}"


# ============================================================
# DESKTOP / LAPTOP / SERVER / MAC ASSET
# ============================================================

class DesktopAsset(models.Model):

    DEVICE_TYPES = [
        ('DESKTOP', 'Desktop'),
        ('LAPTOP', 'Laptop'),
        ('SERVER', 'Server'),
        ('MAC_DESKTOP', 'Mac Desktop'),
        ('MACBOOK', 'MacBook'),
        ('WORKSTATION', 'Workstation'),
        ('MINI_PC', 'Mini PC'),
    ]

    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        related_name='desktop_details'
    )

    asset_type = models.CharField(
        max_length=20,
        choices=DEVICE_TYPES,
        default='DESKTOP',
        db_index=True
    )

    hostname = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        db_index=True
    )

    # PROCESSOR
    processor = models.CharField(max_length=255, blank=True, null=True)
    processor_cores = models.PositiveIntegerField(blank=True, null=True)
    processor_threads = models.PositiveIntegerField(blank=True, null=True)
    processor_speed_mhz = models.PositiveIntegerField(blank=True, null=True)

    # MEMORY & STORAGE
    ram_gb = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    hdd_gb = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    free_disk_gb = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # MOTHERBOARD & BIOS
    bios_version = models.CharField(max_length=150, blank=True, null=True)
    bios_serial_number = models.CharField(max_length=150, blank=True, null=True)
    motherboard = models.CharField(max_length=255, blank=True, null=True)
    graphics_card = models.CharField(max_length=255, blank=True, null=True)

    # OPERATING SYSTEM
    os_installed = models.CharField(max_length=255, blank=True, null=True)
    os_version = models.CharField(max_length=100, blank=True, null=True)
    os_build = models.CharField(max_length=100, blank=True, null=True)

    # WINDOWS LICENSING
    windows_key_last5 = models.CharField(max_length=5, blank=True, null=True)
    windows_license_status = models.CharField(max_length=50, blank=True, null=True)
    license_type = models.CharField(max_length=50, blank=True, null=True)

    # USER & NETWORK
    logged_in_user = models.CharField(max_length=150, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=50, blank=True, null=True)
    system_type = models.CharField(max_length=50, blank=True, null=True)
    domain_name = models.CharField(max_length=200, blank=True, null=True)

    # LAPTOP BATTERY
    battery_name = models.CharField(max_length=150, blank=True, null=True)

    battery_health_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    battery_design_capacity = models.PositiveIntegerField(blank=True, null=True)
    battery_full_charge_capacity = models.PositiveIntegerField(blank=True, null=True)

    # SYNCHRONIZATION
    last_sync = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['asset_type', 'hostname']

    def __str__(self):
        return f"{self.hostname or self.asset} ({self.get_asset_type_display()})"
        
# ============================================================
# COMPUTER DETECTED USER HISTORY
# ============================================================

class ComputerUserHistory(models.Model):

    computer = models.ForeignKey(
        DesktopAsset,
        on_delete=models.CASCADE,
        related_name='detected_user_history'
    )

    # Actual Windows login username
    windows_username = models.CharField(
        max_length=150,
        db_index=True
    )

    # Matched AuraInside employee
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='computer_usage_history'
    )

    # Shift copied from employee record at detection time
    shift = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField()

    is_current = models.BooleanField(
        default=True,
        db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-first_seen']
        indexes = [
            models.Index(
                fields=['computer', 'is_current'],
                name='computer_user_current_idx'
            )
        ]

    def __str__(self):
        return f"{self.computer.hostname} - {self.windows_username}"        

class Monitor(models.Model):
    hostname = models.CharField(max_length=100, db_index=True)
    monitor_id = models.CharField(max_length=150, unique=True)

    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    manufacturer_code = models.CharField(max_length=10, blank=True, null=True)

    model = models.CharField(max_length=150, blank=True, null=True)
    product_code = models.CharField(max_length=50, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)

    screen_size = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )

    connection_type = models.CharField(
        max_length=50, blank=True, null=True
    )

    edid_instance = models.CharField(
        max_length=255, blank=True, null=True
    )

    resolution = models.CharField(
        max_length=30, blank=True, null=True
    )

    refresh_rate = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )

    last_sync = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["hostname", "monitor_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["hostname", "edid_instance"],
                name="unique_monitor_per_hostname_edid",
            )
        ]

    def __str__(self):
        return f"{self.monitor_id} - {self.model or 'Unknown Monitor'}"
