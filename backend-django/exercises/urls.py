from django.urls import path
from .views import (
    ExercisesByGroupView, MuscleGroupCardView, RoutineDetailView,
    RoutineExerciseView, RoutineListCreateView, RoutineReorderView,
    UpdateUserExerciseView, UserExerciseHistoryView, UserExerciseListView,
)

urlpatterns = [
    path('muscle-group-cards/', MuscleGroupCardView.as_view()),
    path('by-group/<str:muscle_group>/', ExercisesByGroupView.as_view()),
    path('user-exercise/<int:user_exercise_id>/', UpdateUserExerciseView.as_view()),
    path('user-exercise/<int:user_exercise_id>/history/', UserExerciseHistoryView.as_view()),
    path('user-exercises/', UserExerciseListView.as_view()),
    path('routines/', RoutineListCreateView.as_view()),
    path('routines/<int:pk>/', RoutineDetailView.as_view()),
    path('routines/<int:pk>/exercises/', RoutineExerciseView.as_view()),
    path('routines/<int:pk>/exercises/<int:re_id>/', RoutineExerciseView.as_view()),
    path('routines/<int:pk>/reorder/', RoutineReorderView.as_view()),
]
