from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Activity, HomePageConfig


class HomeConfigView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        config, _ = HomePageConfig.objects.get_or_create(pk=1)
        activities = Activity.objects.all()

        return Response({
            'hero_title': config.hero_title,
            'about_title': config.about_title,
            'about_description': config.about_description,
            'activities_title': config.activities_title,
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
