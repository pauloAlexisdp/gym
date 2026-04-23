from django.db import models


class HomePageConfig(models.Model):
    hero_title = models.CharField(max_length=200, default='Bienvenido a GymApp')
    about_title = models.CharField(max_length=200, default='Quiénes Somos')
    about_description = models.TextField(default='')
    activities_title = models.CharField(max_length=200, default='Nuestras Actividades')

    background_color = models.CharField(max_length=20, blank=True, default='#f3f4f6')
    background_image = models.ImageField(upload_to='backgrounds/', null=True, blank=True)

    map_embed_url = models.TextField(blank=True, default='')
    facebook_url = models.URLField(blank=True, default='')
    instagram_url = models.URLField(blank=True, default='')
    whatsapp_url = models.URLField(blank=True, default='')

    class Meta:
        db_table = 'home_config'
        verbose_name = 'Configuración de inicio'
        verbose_name_plural = 'Configuración de inicio'

    def __str__(self):
        return 'Configuración de inicio'


class Schedule(models.Model):
    title = models.CharField(max_length=200)
    hours = models.TextField(help_text='Una hora por línea, ej: Lunes - Viernes: 06:00 - 22:00')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'schedules'
        ordering = ['order', 'id']
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'

    def __str__(self):
        return self.title


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
