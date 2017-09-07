from django.db import models

class Epoch(models.Model):
    epoch = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

class TenhouGame(models.Model):
    game_id = models.CharField(max_length=255, unique=True)
    epoch = models.CharField(max_length=255)
    when_played = models.DateTimeField()
    lobby = models.IntegerField()
    scores = models.CharField(max_length=255, blank=True)
    url_names = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.game_id
