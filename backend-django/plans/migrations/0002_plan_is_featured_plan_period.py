from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='period',
            field=models.CharField(blank=True, default='', help_text='Ej: / mes, / día', max_length=50),
        ),
        migrations.AddField(
            model_name='plan',
            name='is_featured',
            field=models.BooleanField(default=False, help_text='Mostrar badge "Más Popular"'),
        ),
    ]
