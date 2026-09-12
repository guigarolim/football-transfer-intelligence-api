from django.db import models
from clubs.models import Club

FOOT_CHOICES = [
    ('R', 'Right'),
    ('L', 'Left'),
    ('B', 'Both'),
]

POSITION_CHOICES = [
    ('GK', 'Goalkeeper'),
    ('CB', 'Center Back'),
    ('LB', 'Left Back'),
    ('RB', 'Right Back'),
    ('DM', 'Defensive Midfielder'),
    ('CM', 'Central Midfielder'),
    ('AM', 'Attacking Midfielder'),
    ('LW', 'Left Winger'),
    ('RW', 'Right Winger'),
    ('ST', 'Striker'),
]

class Player(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    birth_date = models.DateField()
    height = models.FloatField()
    weight = models.FloatField()
    preferred_foot = models.CharField(max_length=1, choices=FOOT_CHOICES)
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    current_club = models.ForeignKey(
    Club,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="players")

    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name

class PlayerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="stats")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="stats")
    goals = models.PositiveSmallIntegerField(default=0)
    assists = models.PositiveSmallIntegerField(default=0)
    matches_played = models.PositiveSmallIntegerField(default=0)
    minutes_played = models.PositiveSmallIntegerField(default=0)
    yellow_cards = models.PositiveSmallIntegerField(default=0)
    red_cards = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.player.name} - {self.season.name}"