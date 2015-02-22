from django.db import models

class TenhouPlayer(models.Model):
    tenhou_name = models.CharField(max_length=255, unique=True)
    primary_id = models.ForeignKey('TenhouPlayer', null=True)

class TenhouGame(models.Model):
    game_id = models.CharField(max_length=255, unique=True)
    date_played = models.DateField()
    lobby = models.IntegerField()
    players = models.ManyToManyField(TenhouPlayer)

    def __str__(self):
        return self.game_id
