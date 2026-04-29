from django.db import models


class Plan(models.Model):
    title = models.CharField(max_length=200)
    price = models.CharField(max_length=50, help_text='Ej: $55.900')
    image = models.ImageField(upload_to='plans/', null=True, blank=True)
    description = models.TextField(blank=True, default='', help_text='Descripción opcional del plan')
    period = models.CharField(max_length=50, blank=True, default='', help_text='Ej: / mes, / día')
    is_featured = models.BooleanField(default=False, help_text='Mostrar badge "Más Popular"')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'plans'
        ordering = ['order', 'id']
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'

    def __str__(self):
        return self.title
