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
from stats.views import decorate_for_template

for game in TenhouGame.objects.all():
    decorate_for_template(game)
    print(game.game_id, game.rounds)
