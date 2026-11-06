
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class FloatingFlag(models.Model):

    POSITION_CHOICES = [
        ("top_left", "Top Left"),
        ("top_center", "Top Center"),
        ("top_right", "Top Right"),
        ("center", "Center"),
        ("bottom_left", "Bottom Left"),
        ("bottom_center", "Bottom Center"),
        ("bottom_right", "Bottom Right"),
        ("custom", "Custom Position"),
    ]

    DIRECTION_CHOICES = [
        ("horizontal", "Horizontal"),
        ("vertical", "Vertical"),
        ("both", "Both"),
    ]

    # Basic details
    title = models.CharField(max_length=150)
    image = models.ImageField(
        upload_to="flags/",
        blank=True,
        null=True
    )
    color = models.CharField(max_length=20, default="#ffffff")

    # Display settings
    position_type = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default="top_right"
    )

    width = models.PositiveIntegerField(
        default=600,
        validators=[MinValueValidator(100), MaxValueValidator(2000)]
    )

    height = models.PositiveIntegerField(
        default=300,
        validators=[MinValueValidator(50), MaxValueValidator(1200)]
    )

    pos_x = models.FloatField(default=50)
    pos_y = models.FloatField(default=10)

    # Cloth animation settings
    camera_angle = models.FloatField(default=0)

    wave_horizontal = models.FloatField(
        default=0.5,
        validators=[MinValueValidator(0), MaxValueValidator(2)]
    )

    wave_vertical = models.FloatField(
        default=0.3,
        validators=[MinValueValidator(0), MaxValueValidator(2)]
    )

    wave_strength = models.FloatField(
        default=0.4,
        validators=[MinValueValidator(0), MaxValueValidator(2)]
    )

    wave_speed = models.FloatField(
        default=0.5,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    animation_direction = models.CharField(
        max_length=20,
        choices=DIRECTION_CHOICES,
        default="both"
    )

    animation_enabled = models.BooleanField(default=True)

    # Layer control
    z_index = models.PositiveIntegerField(default=999)

    # Close button and auto dismissal
    show_close_button = models.BooleanField(default=True)
    auto_close = models.BooleanField(default=False)

    auto_close_seconds = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(3600)]
    )

    # Display scheduling
    start_date = models.DateTimeField(
        blank=True,
        null=True
    )

    end_date = models.DateTimeField(
        blank=True,
        null=True
    )

    # Status
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Floating Flag"
        verbose_name_plural = "Floating Flags"

    def __str__(self):
        return self.title

    @property
    def is_currently_active(self):
        now = timezone.now()

        if not self.is_active:
            return False

        if self.start_date and now < self.start_date:
            return False

        if self.end_date and now > self.end_date:
            return False

        return True


class FloatingFlagDismissal(models.Model):

    flag = models.ForeignKey(
        FloatingFlag,
        on_delete=models.CASCADE,
        related_name="dismissals"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="floating_flag_dismissals"
    )

    dismissed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-dismissed_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["flag", "user"],
                name="unique_floating_flag_user_dismissal"
            )
        ]

    def __str__(self):
        return f"{self.user} dismissed {self.flag.title}"
