from rest_framework import generics
from .models import Player, Season, PlayerStats
from .serializers import PlayerSerializer, PlayerStatsSerializer, SeasonSerializer

class PlayerListView(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetailView(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class SeasonListView(generics.ListAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

class SeasonDetailView(generics.RetrieveAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

class PlayerStatsListView(generics.ListAPIView):
    queryset = PlayerStats.objects.all()
    serializer_class = PlayerStatsSerializer

class PlayerStatsDetailView(generics.RetrieveAPIView):
    queryset = PlayerStats.objects.all()
    serializer_class = PlayerStatsSerializer