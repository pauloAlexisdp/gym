# Generated manually on 2026-04-22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_schedule_remove_homepageconfig_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepageconfig',
            name='background_color',
            field=models.CharField(blank=True, default='#f3f4f6', max_length=20),
        ),
        migrations.AddField(
            model_name='homepageconfig',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to='backgrounds/'),
        ),
    ]
