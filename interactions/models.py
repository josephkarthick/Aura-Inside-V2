from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint
User = settings.AUTH_USER_MODEL


class Reaction(models.Model):
    """
    Stores emoji reactions (👍 🎉 ❤️ 👏) for any content
    like birthday, joinee, announcement, etc.
    """

    REACTION_CHOICES = [
        ("👍", "Like"),
        ("🎉", "Celebrate"),
        ("❤️", "Love"),
        ("👏", "Clap"),
    ]

    # WHO reacted
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reactions"
    )

    # WHAT reaction
    reaction = models.CharField(
        max_length=5,
        choices=REACTION_CHOICES
    )

    # WHERE the reaction happened
    content_type = models.CharField(
        max_length=50,
        db_index=True
    )  # birthday, joinee, announcement

    object_id = models.PositiveIntegerField(
        db_index=True
    )  # user.id / announcement.id

    created_at = models.DateTimeField(auto_now_add=True)

    
    
    class Meta:
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                fields=["user", "content_type", "object_id"],
                name="unique_user_reaction_per_object"
            )
        ]
    


    def __str__(self):
        return f"{self.user} reacted {self.reaction} on {self.content_type}:{self.object_id}"


class Comment(models.Model):
    """
    Stores comments for any content
    like birthday, joinee, announcement, etc.
    """

    # WHO commented
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    # COMMENT text
    text = models.TextField()

    # WHERE the comment belongs
    content_type = models.CharField(
        max_length=50,
        db_index=True
    )

    object_id = models.PositiveIntegerField(
        db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.user} on {self.content_type}:{self.object_id}"
