from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from .models import Exercise, UserExercise


@receiver(post_save, sender=Exercise)
def assign_exercise_to_all_users(sender, instance, created, **kwargs):
    if not created:
        return
    users = User.objects.filter(is_active=True)
    UserExercise.objects.bulk_create(
        [UserExercise(user=user, exercise=instance) for user in users],
        ignore_conflicts=True,
    )


@receiver(post_save, sender=User)
def assign_all_exercises_to_user(sender, instance, created, **kwargs):
    if not created:
        return
    exercises = Exercise.objects.filter(is_active=True)
    UserExercise.objects.bulk_create(
        [UserExercise(user=instance, exercise=exercise) for exercise in exercises],
        ignore_conflicts=True,
    )
