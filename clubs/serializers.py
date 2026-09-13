from rest_framework import serializers
from .models import League
from .models import Club

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'

class ClubSerializer(serializers.ModelSerializer):
    leagues = LeagueSerializer(many=True, read_only=True)
    class Meta:
        model = Club
        fields = '__all__'

