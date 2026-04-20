import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User

email = 'p.parraguez.diaz@hotmail.cl'
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        username='admin',
        email=email,
        password='12345678',
        first_name='Admin',
        last_name='',
    )
    print('Superusuario creado')
else:
    print('Superusuario ya existe')
