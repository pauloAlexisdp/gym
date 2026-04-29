from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Plan


class PlanListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        plans = Plan.objects.filter(is_active=True)
        return Response([
            {
                'id': p.id,
                'title': p.title,
                'price': p.price,
                'description': p.description,
                'period': p.period,
                'is_featured': p.is_featured,
                'image': request.build_absolute_uri(p.image.url) if p.image else None,
            }
            for p in plans
        ])
