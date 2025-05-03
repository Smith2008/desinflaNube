from django.urls import path
from .views import CostView

urlpatterns = [
    path('costs/', CostView.as_view(), name='costs'),
]
