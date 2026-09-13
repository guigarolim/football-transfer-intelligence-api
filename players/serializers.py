from rest_framework import serializers
from .models import Player
from clubs.serializers import ClubSerializer
from .models import Season

class PlayerSerializer(serializers.ModelSerializer):
    current_club = ClubSerializer(allow_null=True, read_only=True)
    class Meta:
        model = Player
        fields = '__all__'

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'
        
