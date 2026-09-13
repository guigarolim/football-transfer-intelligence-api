from rest_framework import serializers
from .models import Player, Season, PlayerStats
from clubs.serializers import ClubSerializer


class PlayerSerializer(serializers.ModelSerializer):
    current_club = ClubSerializer(allow_null=True, read_only=True)
    class Meta:
        model = Player
        fields = '__all__'

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'

class PlayerStatsSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    season = SeasonSerializer(read_only=True)
    class Meta:
        model = PlayerStats
        fields = '__all__'

