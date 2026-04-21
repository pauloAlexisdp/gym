from django.db import models
from users.models import User


class Muscle(models.TextChoices):
    PECTORAL = 'PECTORAL', 'Pectoral'
    DORSAL = 'DORSAL', 'Dorsal'
    BICEPS = 'BICEPS', 'Bíceps'
    TRICEPS = 'TRICEPS', 'Tríceps'
    HOMBRO = 'HOMBRO', 'Hombro'
    CUADRICEPS = 'CUADRICEPS', 'Cuádriceps'
    FEMORALES = 'FEMORALES', 'Femorales'
    GLUTEOS = 'GLUTEOS', 'Glúteos'
    ABDOMINALES = 'ABDOMINALES', 'Abdominales'
    GASTROCNEMIO = 'GASTROCNEMIO', 'Gastrocnemio'

class Days(models.TextChoices):
    LUNES = 'LUNES', 'Lunes'
    MARTES = 'MARTES', 'Martes'
    MIERCOLES = 'MIERCOLES', 'Miércoles'
    JUEVES = 'JUEVES', 'Jueves'
    VIERNES = 'VIERNES', 'Viernes'
    SABADO = 'SABADO', 'Sábado'


class MuscleGroup(models.TextChoices):
    PECHO_HOMBRO = 'PECHO_HOMBRO', 'Pecho y Hombro'
    PIERNAS = 'PIERNAS', 'Piernas'
    ESPALDA_BICEP = 'ESPALDA_BICEP', 'Espalda y Bícep'


class Exercise(models.Model):
    name = models.CharField(max_length=255, unique=True)
    muscle = models.CharField(max_length=20, choices=Muscle.choices)
    muscle_group = models.CharField(max_length=20, choices=MuscleGroup.choices)
    description = models.TextField()
    video_tutorial = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'exercises'


class UserExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='user_exercises')
    reps = models.IntegerField(default=0)
    weight = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'user_exercises'
        unique_together = ('user', 'exercise')


class MuscleGroupCard(models.Model):
    muscle_group = models.CharField(max_length=20, choices=MuscleGroup.choices, unique=True)
    name = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='muscle_groups/')

    class Meta:
        db_table = 'muscle_group_cards'

    def __str__(self):
        return self.get_muscle_group_display()


class UserExerciseHistory(models.Model):
    user_exercise = models.ForeignKey(UserExercise, on_delete=models.CASCADE, related_name='history')
    reps = models.IntegerField()
    weight = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_exercise_history'


class Routine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routines')
    name = models.CharField(max_length=255)
    day  = models.CharField(max_length=20, choices=Days.choices)

    class Meta:
        db_table = 'routines'


class RoutineExercise(models.Model):
    routine  = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='routine_exercises')
    exercise = models.ForeignKey(UserExercise, on_delete=models.CASCADE, related_name='routine_exercises')
    order    = models.IntegerField(default=0)

    class Meta:
        db_table = 'routine_exercises'
        ordering = ['order']
        unique_together = ('routine', 'exercise')
