from django.db import models


class League(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    tier = models.PositiveSmallIntegerField(help_text="1 for top division, 2 for second division, etc.")

    def __str__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    stadium_name = models.CharField(max_length=150, null=True, blank=True)
    crest_url = models.URLField(null=True, blank=True)
    leagues = models.ManyToManyField(League, related_name="clubs")

    def __str__(self):
        return self.name