from django.urls import path
from .views import LeagueListView, LeagueDetailView, ClubListView, ClubDetailView

urlpatterns = [
    path('leagues/', LeagueListView.as_view(), name='league-list'),
    path('leagues/<int:pk>/', LeagueDetailView.as_view(), name='league-detail'),
    path('clubs/', ClubListView.as_view(), name='club-list'),
    path('clubs/<int:pk>/', ClubDetailView.as_view(), name='club-detail'),
]

