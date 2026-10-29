from django.db import models
from django_summernote.fields import SummernoteTextField
from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from django.db import models
from django.utils.timezone import now
from Accounts.models import AuraInsideUser 
from django.utils import timezone


class Tkt_Cat(models.Model):
    category = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category

class Priority_Choice(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, blank=True) 
    weight = models.IntegerField(default=1)  

    def __str__(self):
        return self.name        

class Tkt_SubCat(models.Model):
    category = models.ForeignKey(Tkt_Cat, on_delete=models.CASCADE, related_name="subcategories")
    subcategory = models.CharField(max_length=50)
    priority = models.ForeignKey(Priority_Choice, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.category} - {self.subcategory}" 


class New_Tkt(models.Model):
    ticket_id = models.CharField(
        max_length=20,
        unique=True,
    )

    reported_by = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reported_tickets",
    )

    affected_user = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="affected_tickets",
    )

    asset_type = models.ForeignKey(
        "AssetCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )

    asset = models.ForeignKey(
        "ITAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )

    category = models.ForeignKey(
        Tkt_Cat,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )

    subcategory = models.ForeignKey(
        Tkt_SubCat,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    priority = models.ForeignKey(
        Priority_Choice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )

    status = models.CharField(
        max_length=30,
        default="NEW",
    )

    assigned_to = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.ticket_id
 


class TicketHistory(models.Model):
    ticket = models.ForeignKey(New_Tkt, on_delete=models.CASCADE, related_name="history")
    previous_status = models.CharField(max_length=20,null=True)
    new_status = models.CharField(max_length=20,null=True)
    changed_by = models.CharField(max_length=20,null=True)
    changed_at = models.DateTimeField(default=now)
    notes = models.TextField(blank=True, null=True)  
    status_updated_at = models.DateTimeField(blank=True, null=True) 
    status_updated_by = models.CharField(max_length=20,null=True) 
    assigned_to = models.CharField(max_length=20,null=True) 

    def __str__(self):
        return f"{self.ticket.ticket_id}: {self.previous_status} → {self.new_status} by {self.changed_by}"


class RenewalHeading(models.Model):
    heading = models.CharField(max_length=255)

    def __str__(self):
        return self.heading

class Renewal(models.Model):
    heading = models.ForeignKey(RenewalHeading, on_delete=models.CASCADE, related_name='renewals')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    renewal_date = models.DateTimeField(blank=True,null=True)
    is_renewed = models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.title
        
class Vendor(models.Model):
    name = models.CharField(max_length=200)
    gst_number = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name        

class Invoice(models.Model):
    invoice_no = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="invoices")
    date_of_purchase = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    uploaded_copy = models.FileField(upload_to="invoices/", blank=True, null=True)
    remarks = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)    

    def __str__(self):
        return f"{self.invoice_no} - {self.vendor if self.vendor else 'No Vendor'}"
        
class AssetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_managed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
        

class ITAsset(models.Model):

    STATUS_CHOICES = [
        ("in_stock", "In Stock"),
        ("in_use", "In Use"),
        ("repair", "Under Repair"),
        ("damaged", "Damaged"),
        ("disposed", "Disposed"),
    ]

    # ============================
    # Business Information
    # ============================

    asset_tag = models.CharField(max_length=100, unique=True, null=True,)

    product_name = models.CharField(max_length=200,null=True,)

    category = models.ForeignKey(
        "AssetCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assets",
    )

    warranty_expiry = models.DateField(blank=True, null=True)

    location = models.CharField(max_length=200, blank=True, null=True)

    remarks = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_stock",
    )

    # ============================
    # Hardware Information
    # (Auto updated by Agent if Managed=True)
    # ============================

    hostname = models.CharField(max_length=100, unique=True, blank=True, null=True)

    manufacturer = models.CharField(max_length=100, blank=True, null=True)

    brand = models.CharField(max_length=100, blank=True, null=True)

    model = models.CharField(max_length=150, blank=True, null=True)

    serial_number = models.CharField(max_length=150, blank=True, null=True)

    processor = models.CharField(max_length=255, blank=True, null=True)

    ram_gb = models.IntegerField(blank=True, null=True)

    hdd_gb = models.IntegerField(blank=True, null=True)

    free_disk_gb = models.IntegerField(blank=True, null=True)

    os_installed = models.CharField(max_length=100, blank=True, null=True)

    windows_key_last5 = models.CharField(max_length=10, blank=True, null=True)

    windows_license_status = models.CharField(max_length=50, blank=True, null=True)

    license_type = models.CharField(max_length=100, blank=True, null=True)

    bios_version = models.CharField(max_length=100, blank=True, null=True)

    system_type = models.CharField(max_length=100, blank=True, null=True)

    domain_name = models.CharField(max_length=100, blank=True, null=True)

    ip_address = models.GenericIPAddressField(blank=True, null=True)

    mac_address = models.CharField(max_length=50, blank=True, null=True)

    logged_in_user = models.CharField(max_length=100, blank=True, null=True)


    # ============================
    # Audit
    # ============================

    created_at = models.DateTimeField(auto_now_add=True, null=True,)

    last_updated = models.DateTimeField(auto_now=True, null=True,)

    def __str__(self):
        return f"{self.asset_tag} - {self.product_name}"
        
class Monitor(models.Model):

    asset = models.ForeignKey(
        ITAsset,
        on_delete=models.CASCADE,
        related_name="monitors"
    )

    monitor_number = models.PositiveIntegerField(default=1)

    manufacturer = models.CharField(
        max_length=100,
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

    resolution = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    refresh_rate = models.IntegerField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["monitor_number"]

    def __str__(self):
        return f"{self.asset.hostname} - Monitor {self.monitor_number}"        
        
        
class VoIPAPI(models.Model):
    vendor = models.OneToOneField(
        Vendor,
        on_delete=models.CASCADE,
        related_name='voip_api'
    )

    api_token = models.TextField()
    click_to_call_url = models.URLField(max_length=500)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.vendor.name} VoIP API"        


class VoipRecord(models.Model):
    vendor = models.ForeignKey(
        "Vendor",
        on_delete=models.CASCADE,
        related_name="voip_records",
    )

    callback_number = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    domain = models.CharField(max_length=150)

    cdr_id = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    is_free = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    empid = models.ForeignKey(
        "Accounts.AuraInsideUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="voip_accounts",
    )

    tenant_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    company_code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    url_webrtc = models.CharField(
        max_length=500,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.username} ({self.vendor.name})"

  