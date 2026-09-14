from django.urls import path
from .views import PlayerListView, PlayerDetailView, SeasonListView, SeasonDetailView, PlayerStatsListView, PlayerStatsDetailView

urlpatterns = [
    path('players/', PlayerListView.as_view(), name = 'player-list'),
    path('players/<int:pk>/', PlayerDetailView.as_view(), name = 'player-detail'),
    path('seasons/', SeasonListView.as_view(), name = 'season-list'),
    path('seasons/<int:pk>/', SeasonDetailView.as_view(), name = 'season-detail'),
    path('players-stats/', PlayerStatsListView.as_view(), name = 'playerstats-list'),
    path('players-stats/<int:pk>/', PlayerStatsDetailView.as_view(), name = 'playerstats-detail'),
]