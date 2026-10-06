from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    KIND_CHOICES = [
        ('booking_confirmed', 'Reserva confirmada'),
        ('reminder', 'Recordatorio de reserva'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    kind = models.CharField(max_length=30, choices=KIND_CHOICES)
    title = models.CharField(max_length=200)
    body = models.TextField()
    reservation = models.ForeignKey(
        'reservas.Reservation',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
    )
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'read']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.title}"