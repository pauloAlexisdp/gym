from django.urls import path
from .views import HomeConfigView

urlpatterns = [
    path('config/', HomeConfigView.as_view()),
]
