#!/usr/bin/python3

import codecs
import os
import sys

sys.stdout = codecs.getwriter('utf8')(sys.stdout.detach())

import django
os.environ["DJANGO_SETTINGS_MODULE"] = "mjapp.settings"
django.setup()

from django.conf import settings
from stats.models import TenhouGame, TenhouPlayer
from stats.views import process_game

TenhouPlayer.objects.all().delete()
for game in TenhouGame.objects.all():
    print(game.game_id)
    fname = "{}/{}.xml".format(settings.TENHOU_LOG_DIR, game.game_id)
    process_game(game.game_id, fname, game.epoch, game)
