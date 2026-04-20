from django.db import models


class HomePageConfig(models.Model):
    hero_title = models.CharField(max_length=200, default='Bienvenido a GymApp')
    about_title = models.CharField(max_length=200, default='Quiénes Somos')
    about_description = models.TextField(default='')
    activities_title = models.CharField(max_length=200, default='Nuestras Actividades')

    class Meta:
        db_table = 'home_config'
        verbose_name = 'Configuración de inicio'
        verbose_name_plural = 'Configuración de inicio'

    def __str__(self):
        return 'Configuración de inicio'


class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='activities/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'activities'
        ordering = ['order', 'id']
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    def __str__(self):
        return self.title
