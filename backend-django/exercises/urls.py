from django.urls import path
from .views import ExercisesByGroupView, MuscleGroupCardView, UpdateUserExerciseView, UserExerciseHistoryView

urlpatterns = [
    path('muscle-group-cards/', MuscleGroupCardView.as_view()),
    path('by-group/<str:muscle_group>/', ExercisesByGroupView.as_view()),
    path('user-exercise/<int:user_exercise_id>/', UpdateUserExerciseView.as_view()),
    path('user-exercise/<int:user_exercise_id>/history/', UserExerciseHistoryView.as_view()),
]
