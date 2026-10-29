from django.db import models
from Accounts.models import AuraInsideUser 
from django.db import models
import uuid

id = uuid.uuid4()

def get_user_fields():
    """Return all field names from AuraInsideUser except system ones."""
    exclude_fields = ['id', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined']
    return [(f.name, f.verbose_name.title()) for f in AuraInsideUser._meta.fields if f.name not in exclude_fields]

PHOTO_LAYOUT_CHOICES = [
    ('1', 'Full Width (1 per row)'),
    ('2', 'Two per row'),
    ('3', 'Three per row'),
    ('4', 'Four per row'),
]

class Home(models.Model):
    CONTENT_TYPES = [
        ('news', 'News'),
        ('event', 'Event'),
        ('announcement', 'Announcement'),
        ('Birthday', 'Birthday'),
        ('Work Anniversaries', 'Work Anniversaries'),
        ('Recruitment Update', 'Recruitment Update'),
        ('New joinees ', 'New joinees'),
    ]

    PHOTO_SIZES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES,null=True, blank=True)
    title = models.CharField(max_length=255,null=True, blank=True)
    photo = models.ImageField(upload_to="home_banners/",null=True, blank=True)
    username = models.ForeignKey(AuraInsideUser, on_delete=models.CASCADE,null=True, blank=True)
    project = models.CharField(max_length=255, blank=True,null=True)
    field1 = models.CharField(max_length=100, choices=get_user_fields(), null=True, blank=True)
    field2 = models.CharField(max_length=100, choices=get_user_fields(), null=True, blank=True)
    description = models.TextField(null=True, blank=True,)
    photo_layout = models.CharField(max_length=1, choices=PHOTO_LAYOUT_CHOICES, default='1',null=True, blank=True)  # New field
    show = models.BooleanField(default=True,null=True, blank=True, help_text="Tick to display this item on the homepage")
    order_no = models.PositiveIntegerField(default=0,null=True, blank=True, help_text="Lower numbers appear first")

    def __str__(self):
        return self.title

    def get_field_value(self, field_name):
        """Return the value of the selected field for the selected user."""
        return getattr(self.username, field_name, '')

class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class BoardMembers(models.Model):

    CHART_TYPE_CHOICES = (
        ('operation', 'Operation'),
        ('management', 'Management'),
    )

    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='board_members/', blank=True, null=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    chart_type = models.CharField(
        max_length=20,
        choices=CHART_TYPE_CHOICES,
        default='operation'
    )

    def __str__(self):
        return self.name



class GalleryGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g. Christmas, Diwali, New Year")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

import os
from PIL import Image
from django.db import models

# Dynamic upload path (per group)
def festival_image_path(instance, filename):
    folder_name = instance.group.name.replace(" ", "_")
    return os.path.join("festival_gallery", folder_name, "original", filename)

def festival_thumb_path(instance, filename):
    folder_name = instance.group.name.replace(" ", "_")
    return os.path.join("festival_gallery", folder_name, "thumbs", filename)


class Gallery(models.Model):
    group = models.ForeignKey(
        GalleryGroup,
        on_delete=models.CASCADE,
        related_name="images"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # Original image (FULL quality)
    image = models.ImageField(upload_to=festival_image_path)

    # Thumbnail (LIGHTWEIGHT)
    thumbnail = models.ImageField(
        upload_to=festival_thumb_path,
        blank=True,
        null=True
    )

    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.group.name} - {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image and not self.thumbnail:
            self.generate_thumbnail()

    def generate_thumbnail(self):
        img = Image.open(self.image.path)
        img = img.convert("RGB")

        # ✅ PERFECT gallery size
        img.thumbnail((600, 600))

        filename = os.path.basename(self.image.name)
        thumb_path = os.path.join(
            os.path.dirname(self.image.path).replace("original", "thumbs"),
            filename
        )

        os.makedirs(os.path.dirname(thumb_path), exist_ok=True)

        # ✅ KEY PERFORMANCE SETTING
        img.save(
            thumb_path,
            "JPEG",
            quality=70,       # 👈 balance quality & speed
            optimize=True
        )

        self.thumbnail = thumb_path.replace(
            os.path.dirname(self.image.path).split("festival_gallery")[0],
            ""
        )

        super().save(update_fields=["thumbnail"])


class FloatingFlag(models.Model):
    title = models.CharField(max_length=100, default="Aura Flag")

    camera_angle = models.FloatField(default=0)

    image = models.ImageField(upload_to="flags/", blank=True, null=True)
    color = models.CharField(max_length=7, default="#ffffff")

    width = models.FloatField(default=30)
    height = models.FloatField(default=20)

    pos_x = models.IntegerField(default=200)
    pos_y = models.IntegerField(default=200)

    wave_horizontal = models.FloatField(default=0.5)
    wave_vertical = models.FloatField(default=0.3)
    wave_strength = models.FloatField(default=0.2)
    wave_speed = models.FloatField(default=0.5)

    is_active = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

