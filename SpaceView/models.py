from django.db import models

class Workstation(models.Model):
    FLOOR_CHOICES = [
        ("eighth", "Guna Complex - Eighth Floor"),
        ("second", "Second Map"),
    ]

    workstation_code = models.CharField(max_length=20)

    floor = models.CharField(
        max_length=20,
        choices=FLOOR_CHOICES,
    )

    x_position = models.FloatField()
    y_position = models.FloatField()

    # Stores the ITDesk asset ID without a database foreign key.
    assigned_asset_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        db_index=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["floor", "workstation_code"]
        constraints = [
            models.UniqueConstraint(
                fields=["floor", "workstation_code"],
                name="unique_workstation_code_per_floor",
            ),
        ]

    def __str__(self):
        return f"{self.workstation_code} - {self.get_floor_display()}"
