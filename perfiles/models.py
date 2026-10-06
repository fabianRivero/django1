from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ('admin', 'Administrador'),
    ('client', 'Cliente'),
)

# clase que representa el perfil del usuario
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default="client")

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    @classmethod
    def create_profile(cls, user):
        return cls.objects.create(user=user)

    def __str__(self):
        return self.user.username   

