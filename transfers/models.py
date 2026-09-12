from django.db import models
from clubs.models import Club
from players.models import Player

TRANSFER_CHOICES = [
    ('P', 'Permanent'),
    ('L', 'Loan'),
    ('F', 'Free'),
]

class Transfer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="transfers")
    from_club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, related_name="transfers_out")
    to_club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, related_name="transfers_in")
    date = models.DateField()
    fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    transfer_type = models.CharField(max_length=1, choices=TRANSFER_CHOICES)

    def __str__(self):
        destination = self.to_club.name if self.to_club else "Free Agent"
        return f"{self.player.name} - {destination}"
    
