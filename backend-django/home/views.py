from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Activity, HomePageConfig, Schedule


class HomeConfigView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        config, _ = HomePageConfig.objects.get_or_create(pk=1)
        activities = Activity.objects.all()
        schedules = Schedule.objects.all()

        return Response({
            'hero_title': config.hero_title,
            'about_title': config.about_title,
            'about_description': config.about_description,
            'activities_title': config.activities_title,
            'schedules': [
                {'title': s.title, 'hours': s.hours}
                for s in schedules
            ],
            'background_color': config.background_color,
            'background_image': request.build_absolute_uri(config.background_image.url) if config.background_image else None,
            'map_embed_url': config.map_embed_url,
            'facebook_url': config.facebook_url,
            'instagram_url': config.instagram_url,
            'whatsapp_url': config.whatsapp_url,
            'activities': [
                {
                    'id': a.id,
                    'title': a.title,
                    'description': a.description,
                    'image': request.build_absolute_uri(a.image.url) if a.image else None,
                }
                for a in activities
            ],
        })
