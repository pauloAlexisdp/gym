from django.contrib import admin
from .models import Exercise, MuscleGroupCard, UserExercise, UserExerciseHistory


@admin.register(MuscleGroupCard)
class MuscleGroupCardAdmin(admin.ModelAdmin):
    list_display = ('muscle_group', 'image')



@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'muscle', 'muscle_group', 'is_active')
    list_filter = ('muscle', 'muscle_group', 'is_active')
    search_fields = ('name',)


@admin.register(UserExercise)
class UserExerciseAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'reps', 'weight')
    list_filter = ('exercise',)
    search_fields = ('user__email', 'exercise__name')


@admin.register(UserExerciseHistory)
class UserExerciseHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_exercise', 'reps', 'weight', 'date')
    list_filter = ('date',)
    ordering = ('-date',)
