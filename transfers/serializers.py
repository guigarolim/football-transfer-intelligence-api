from rest_framework import serializers
from .models import Transfer
from clubs.serializers import ClubSerializer
from players.serializers import PlayerSerializer
 
class TransferSerializer(serializers.ModelSerializer):
    from_club = ClubSerializer(allow_null=True, read_only=True)
    to_club = ClubSerializer(allow_null=True, read_only=True)
    player = PlayerSerializer(read_only=True)
    class Meta:
        model = Transfer
        fields = '__all__'
