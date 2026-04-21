from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MuscleGroupCard, Routine, RoutineExercise, UserExercise, UserExerciseHistory
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


class UserExerciseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_exercises = UserExercise.objects.filter(
            user=request.user, exercise__is_active=True
        ).select_related('exercise').order_by('exercise__name')
        return Response([
            {
                'id': ue.id,
                'name': ue.exercise.name,
                'muscle': ue.exercise.muscle,
                'reps': ue.reps,
                'weight': ue.weight,
            }
            for ue in user_exercises
        ])


class RoutineListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        routines = Routine.objects.filter(user=request.user).prefetch_related(
            'routine_exercises__exercise__exercise'
        )
        data = [self._serialize(r) for r in routines]
        return Response(data)

    def post(self, request):
        name = request.data.get('name', '').strip()
        day  = request.data.get('day', '').strip()
        if not name or not day:
            return Response({'message': 'name y day son requeridos'}, status=status.HTTP_400_BAD_REQUEST)
        routine = Routine.objects.create(user=request.user, name=name, day=day)
        return Response(self._serialize(routine), status=status.HTTP_201_CREATED)

    @staticmethod
    def _serialize(routine):
        return {
            'id': routine.id,
            'name': routine.name,
            'day': routine.day,
            'exercises': [
                {
                    'id': re.id,
                    'order': re.order,
                    'user_exercise_id': re.exercise.id,
                    'exercise_id': re.exercise.exercise.id,
                    'name': re.exercise.exercise.name,
                    'muscle': re.exercise.exercise.muscle,
                    'reps': re.exercise.reps,
                    'weight': re.exercise.weight,
                }
                for re in routine.routine_exercises.all()
            ],
        }


class RoutineDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get(self, request, pk):
        try:
            return Routine.objects.prefetch_related(
                'routine_exercises__exercise__exercise'
            ).get(pk=pk, user=request.user)
        except Routine.DoesNotExist:
            return None

    def get(self, request, pk):
        routine = self._get(request, pk)
        if not routine:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(RoutineListCreateView._serialize(routine))

    def patch(self, request, pk):
        routine = self._get(request, pk)
        if not routine:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if 'name' in request.data:
            routine.name = request.data['name']
        if 'day' in request.data:
            routine.day = request.data['day']
        routine.save()
        return Response(RoutineListCreateView._serialize(routine))

    def delete(self, request, pk):
        routine = self._get(request, pk)
        if not routine:
            return Response(status=status.HTTP_404_NOT_FOUND)
        routine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoutineExerciseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            routine = Routine.objects.get(pk=pk, user=request.user)
        except Routine.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_exercise_id = request.data.get('user_exercise_id')
        try:
            user_exercise = UserExercise.objects.get(id=user_exercise_id, user=request.user)
        except UserExercise.DoesNotExist:
            return Response({'message': 'Ejercicio no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        last_order = routine.routine_exercises.count()
        re, created = RoutineExercise.objects.get_or_create(
            routine=routine,
            exercise=user_exercise,
            defaults={'order': last_order},
        )
        if not created:
            return Response({'message': 'El ejercicio ya está en la rutina'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'id': re.id,
            'order': re.order,
            'user_exercise_id': user_exercise.id,
            'name': user_exercise.exercise.name,
            'reps': user_exercise.reps,
            'weight': user_exercise.weight,
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, re_id):
        try:
            re = RoutineExercise.objects.get(pk=re_id, routine__pk=pk, routine__user=request.user)
        except RoutineExercise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        re.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoutineReorderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            routine = Routine.objects.get(pk=pk, user=request.user)
        except Routine.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        order_list = request.data.get('order', [])
        for idx, re_id in enumerate(order_list):
            RoutineExercise.objects.filter(pk=re_id, routine=routine).update(order=idx)

        return Response(status=status.HTTP_204_NO_CONTENT)


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
