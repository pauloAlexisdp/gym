from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    lastname = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        normalized = value.strip().lower()
        if User.objects.filter(email=normalized).exists():
            raise serializers.ValidationError('El email ya está registrado')
        return normalized

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['name'].strip(),
            last_name=validated_data['lastname'].strip(),
            password=validated_data['password'],
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
