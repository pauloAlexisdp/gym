from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MuscleGroupCard, UserExercise, UserExerciseHistory
from django.utils.timezone import localtime


class MuscleGroupCardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cards = MuscleGroupCard.objects.all()
        data = [
            {
                'id': card.id,
                'muscle_group': card.muscle_group,
                'name': card.name,
                'image': request.build_absolute_uri(card.image.url) if card.image else None,
            }
            for card in cards
        ]
        return Response(data)


class ExercisesByGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, muscle_group):
        user_exercises = UserExercise.objects.filter(
            user=request.user,
            exercise__muscle_group=muscle_group,
            exercise__is_active=True,
        ).select_related('exercise')

        data = [
            {
                'id': ue.exercise.id,
                'user_exercise_id': ue.id,
                'name': ue.exercise.name,
                'description': ue.exercise.description,
                'muscle': ue.exercise.muscle,
                'video_tutorial': ue.exercise.video_tutorial,
                'reps': ue.reps,
                'weight': ue.weight,
            }
            for ue in user_exercises
        ]
        return Response(data)


class UpdateUserExerciseView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_exercise_id):
        try:
            user_exercise = UserExercise.objects.get(id=user_exercise_id, user=request.user)
        except UserExercise.DoesNotExist:
            return Response({'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)

        reps = request.data.get('reps')
        weight = request.data.get('weight')

        if reps is None or weight is None:
            return Response({'message': 'reps y weight son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        user_exercise.reps = reps
        user_exercise.weight = weight
        user_exercise.save()

        UserExerciseHistory.objects.create(
            user_exercise=user_exercise,
            reps=reps,
            weight=weight,
        )

        return Response({'reps': user_exercise.reps, 'weight': user_exercise.weight})


class UserExerciseHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_exercise_id):
        try:
            user_exercise = UserExercise.objects.get(id=user_exercise_id, user=request.user)
        except UserExercise.DoesNotExist:
            return Response({'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)

        history = UserExerciseHistory.objects.filter(
            user_exercise=user_exercise
        ).order_by('date')

        data = [
            {
                'date': localtime(h.date).strftime('%d/%m/%Y'),
                'reps': h.reps,
                'weight': h.weight,
            }
            for h in history
        ]
        return Response(data)
