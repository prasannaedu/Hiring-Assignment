from django.db import models
from app.models.user import User
from app.models.contact import Contact


class Interaction(models.Model):
    INTERACTION_TYPE_CHOICES = [
        ('call', 'Call'),
        ('message', 'Message'),
        ('spam', 'Spam Report'),
    ]

    initiator = models.ForeignKey(
        User,
        related_name='initiated_interactions',
        on_delete=models.CASCADE
    )
    receiver_user = models.ForeignKey(
        User,
        related_name='received_interactions',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    receiver_contact = models.ForeignKey(
        Contact,
        related_name='received_interactions',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    type = models.CharField(max_length=20, choices=INTERACTION_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['initiator']),
            models.Index(fields=['receiver_user']),
            models.Index(fields=['type']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        if self.receiver_user:
            receiver = self.receiver_user.get_full_name()
        elif self.receiver_contact:
            receiver = self.receiver_contact.get_full_name()
        else:
            receiver = "Unknown"
        return f"{self.initiator.get_full_name()} -> {receiver} ({self.type})"
