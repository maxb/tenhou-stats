from django.db import models

class TenhouPlayer(models.Model):
    tenhou_name = models.CharField(max_length=255, unique=True)
    primary_id = models.ForeignKey('TenhouPlayer', null=True)
    rank = models.CharField(max_length=255)
    rate = models.IntegerField()
    rank_time = models.DateTimeField()

    def __str__(self):
        return self.tenhou_name

class TenhouGame(models.Model):
    game_id = models.CharField(max_length=255, unique=True)
    when_played = models.DateTimeField()
    lobby = models.IntegerField()
    players = models.ManyToManyField(TenhouPlayer)
    scores = models.CharField(max_length=255, blank=True)
    url_names = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.game_id
