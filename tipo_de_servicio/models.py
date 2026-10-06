from django.db import models

class TypeOfService(models.Model):
    name = models.CharField(max_length=100)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=30.00)
    with_roof = models.BooleanField(default=False)
    image_path = models.CharField(max_length=128, blank=True)
    
    
    class Meta:
        verbose_name = 'Tipo de servicio'
        verbose_name_plural = 'Tipos de servicio'

    def __str__(self):
        return self.name   

