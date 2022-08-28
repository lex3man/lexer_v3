from django.urls import path
from .views import FeelAction

urlpatterns = [
    path('', FeelAction.as_view()),
]