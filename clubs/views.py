from rest_framework import generics
from .models import League, Club
from .serializers import LeagueSerializer, ClubSerializer

class LeagueListView(generics.ListAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

class LeagueDetailView(generics.RetrieveAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

class ClubListView(generics.ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

class ClubDetailView(generics.RetrieveAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer