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
from stats.views import GAME_ID_RE, process_game

TenhouPlayer.objects.all().delete()
for game in TenhouGame.objects.all():
    print(game.game_id)

    game_id = game.game_id
    m = GAME_ID_RE.match(game_id)
    fname = "{}/{}.xml".format(settings.TENHOU_LOG_DIR, game.game_id)

    process_game(game_id, m, fname, game)
