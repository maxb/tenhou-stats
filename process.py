#!/usr/bin/python3

import codecs
import datetime
import os
import sys
import time
from urllib.parse import urlencode
from xml.etree import ElementTree as ET

sys.stdout = codecs.getwriter('utf8')(sys.stdout.detach())

import django
os.environ["DJANGO_SETTINGS_MODULE"] = "mjapp.settings"
django.setup()

from django.conf import settings
from stats.models import TenhouGame, TenhouPlayer

import TenhouDecoder

for game in TenhouGame.objects.filter(lobby=1303):
    print(game.game_id)
    fname = "{}/{}.xml".format(settings.TENHOU_LOG_DIR, game.game_id)

    with open(fname, 'rb') as f:
        data = f.read()
    etree = ET.fromstring(data)

    with open(fname, 'rb') as f:
        gdata = TenhouDecoder.Game()
        gdata.decode(f)

    # Player and score data
    owari = etree.find('./*[@owari]').get('owari').split(',')
    usernames = []
    scores = []
    uparams = []
    dbplayers = []
    for i, xmlplayer in enumerate(gdata.players):
        print(i, xmlplayer.asdata())
        num = owari[i * 2 + 1]
        if num[0] != '-':
            num = "+" + num
        nx = 'n{}'.format(i)
        username = xmlplayer.name
        usernames.append(username)
        scores.append((username, num, float(num), i))
        uparams.append((nx, username))
        try:
            dbplayer = TenhouPlayer.objects.get(tenhou_name=username)
        except TenhouPlayer.DoesNotExist:
            dbplayer = TenhouPlayer(tenhou_name=username)
        if dbplayer.rank_time is None or game.when_played > dbplayer.rank_time:
            dbplayer.rank_time = game.when_played
            dbplayer.rank = xmlplayer.rank
            dbplayer.rate = xmlplayer.rate
            dbplayer.save()
    scores.sort(key=lambda x: x[2], reverse=True)

    if not game.players.all().exists():
        for dbplayer in dbplayers:
            game.players.add(dbplayer)

    save = False

    when_tt = time.strptime(game.game_id[:10], '%Y%m%d%H')
    when = datetime.datetime(
            year=when_tt.tm_year,
            month=when_tt.tm_mon,
            day=when_tt.tm_mday,
            hour=when_tt.tm_hour)
    if game.when_played != when:
        game.when_played = when
        save = True

    if not game.scores:
        game.scores = " ".join(("{}({})".format(name, score) for name, score, number, playerpos in scores))
        save = True

    if not game.url_names:
        game.url_names = urlencode(uparams)
        save = True

    if save:
        game.save()

    #for r in gdata.rounds:
    #    print(r.round, r.dealer)
    #    for agari in r.agari:
    #        print(agari)
