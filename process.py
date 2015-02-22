#!/usr/bin/python3

import codecs
import datetime
import os
import sys
import time
from urllib.parse import urlencode

sys.stdout = codecs.getwriter('utf8')(sys.stdout.detach())

import django
os.environ["DJANGO_SETTINGS_MODULE"] = "mjapp.settings"
django.setup()

from django.conf import settings
from stats.models import TenhouGame, TenhouPlayer
from stats.views import format_agari, format_round

import TenhouDecoder

for game in TenhouGame.objects.all():
    print(game.game_id)
    fname = "{}/{}.xml".format(settings.TENHOU_LOG_DIR, game.game_id)

    with open(fname, 'rb') as f:
        gdata = TenhouDecoder.Game()
        gdata.decode(f)

    full_stats = game.lobby == 1303 and len(gdata.players) == 4
    owari = gdata.owari.split(',')
    data = []
    urlparams = []
    for i, xmlplayer in enumerate(gdata.players):
        #print(i, xmlplayer.asdata())
        num = owari[i * 2 + 1]
        if num[0] != '-':
            num = "+" + num
        username = xmlplayer.name
        urlparams.append(('n{}'.format(i), username))
        if full_stats:
            try:
                dbplayer = TenhouPlayer.objects.get(tenhou_name=username)
            except TenhouPlayer.DoesNotExist:
                dbplayer = TenhouPlayer(tenhou_name=username)
            if dbplayer.rank_time is None or game.when_played > dbplayer.rank_time:
                dbplayer.rank_time = game.when_played
                dbplayer.rank = xmlplayer.rank
                dbplayer.rate = xmlplayer.rate
            dbplayer.ngames += 1
        else:
            dbplayer = None
        data.append((username, num, float(num), i, dbplayer))

    if full_stats:
        for r in gdata.rounds:
            #print(format_round(r))
            for agari in r.agari:
                #print(format_agari(agari, gdata), agari)
                if hasattr(agari, 'limit'):
                    dbplayer = data[agari.player][4]
                    setattr(dbplayer, 'n' + agari.limit,
                            getattr(dbplayer, 'n' + agari.limit) + 1)

        data.sort(key=lambda x: x[2], reverse=True)
        data[0][4].nplace1 += 1
        data[1][4].nplace2 += 1
        data[2][4].nplace3 += 1
        data[3][4].nplace4 += 1

        for _, _, _, _, dbplayer in data:
            dbplayer.save()

        if not game.players.all().exists():
            for _, _, _, _, dbplayer in data:
                game.players.add(dbplayer)
    else:
        data.sort(key=lambda x: x[2], reverse=True)


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
        game.scores = " ".join(("{}({})".format(name, score) for name, score, _, _, _ in data))
        save = True

    if not game.url_names:
        game.url_names = urlencode(urlparams)
        save = True

    if save:
        game.save()
