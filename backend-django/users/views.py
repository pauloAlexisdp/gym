import os

import resend
from django.conf import settings
from django.utils.timezone import localtime
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PasswordResetToken, User, WeightHistory, WhitelistedEmail
from .serializers import LoginSerializer, RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        if not WhitelistedEmail.objects.filter(email=email).exists():
            return Response({'message': 'Este email no está autorizado para registrarse'}, status=status.HTTP_403_FORBIDDEN)

        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            first_field = next(iter(serializer.errors))
            message = serializer.errors[first_field][0]
            return Response({'message': str(message)}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        return Response({
            'message': 'Usuario registrado exitosamente',
            'data': {
                'id': user.id,
                'name': user.first_name,
                'lastname': user.last_name,
                'email': user.email,
                'role': user.role,
                'isActive': user.is_active,
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            first_field = next(iter(serializer.errors))
            message = serializer.errors[first_field][0]
            return Response({'message': str(message)}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email'].strip().lower()
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({'message': 'Usuario inactivo'}, status=status.HTTP_403_FORBIDDEN)

        if not user.check_password(password):
            return Response({'message': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)

        token = str(RefreshToken.for_user(user).access_token)

        return Response({
            'message': 'Inicio de sesión exitoso',
            'data': {
                'token': token,
                'user': {
                    'id': user.id,
                    'name': user.first_name,
                    'lastname': user.last_name,
                    'email': user.email,
                    'role': user.role,
                    'isActive': user.is_active,
                    'profile_picture': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
                }
            }
        })


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({'message': 'Si el email existe, recibirás un enlace de recuperación.'})

        reset_token = PasswordResetToken.objects.create(user=user)
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        reset_url = f'{frontend_url}/reset-password?token={reset_token.token}'

        resend.api_key = settings.RESEND_API_KEY
        resend.Emails.send({
            'from': 'onboarding@resend.dev',
            'to': [user.email],
            'subject': 'Recuperar contraseña',
            'html': f'''
                <p>Hola {user.first_name},</p>
                <p>Recibimos una solicitud para restablecer tu contraseña.</p>
                <p><a href="{reset_url}" style="background:#000;color:#fff;padding:10px 20px;border-radius:6px;text-decoration:none;">Restablecer contraseña</a></p>
                <p>Este enlace expira en 1 hora. Si no solicitaste esto, ignora este mensaje.</p>
            ''',
        })

        return Response({'message': 'Si el email existe, recibirás un enlace de recuperación.'})


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        password = request.data.get('password')

        if not token or not password:
            return Response({'message': 'Token y contraseña son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reset_token = PasswordResetToken.objects.select_related('user').get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response({'message': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)

        if not reset_token.is_valid():
            return Response({'message': 'El token ha expirado o ya fue usado'}, status=status.HTTP_400_BAD_REQUEST)

        user = reset_token.user
        user.set_password(password)
        user.save()

        reset_token.used = True
        reset_token.save()

        return Response({'message': 'Contraseña actualizada correctamente'})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def _user_data(self, request, user):
        return {
            'id': user.id,
            'name': user.first_name,
            'lastname': user.last_name,
            'email': user.email,
            'height': user.height,
            'profile_picture': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
        }

    def get(self, request):
        return Response(self._user_data(request, request.user))

    def patch(self, request):
        user = request.user
        if 'height' in request.data:
            user.height = request.data['height']
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        user.save()
        return Response(self._user_data(request, user))


class WeightHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entries = WeightHistory.objects.filter(user=request.user)
        return Response([
            {'date': localtime(e.date).strftime('%d/%m/%Y'), 'weight': float(e.weight)}
            for e in entries
        ])

    def post(self, request):
        weight = request.data.get('weight')
        if not weight:
            return Response({'message': 'weight es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        entry = WeightHistory.objects.create(user=request.user, weight=weight)
        return Response({'date': localtime(entry.date).strftime('%d/%m/%Y'), 'weight': float(entry.weight)})
