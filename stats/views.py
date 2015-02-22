from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

import datetime
import os
import re
import time

from .models import TenhouGame

def stats_home(request):
    games_by_day = []
    current_day = None
    games_current_day = None
    for game in TenhouGame.objects.filter(lobby=1303).order_by('-when_played'):
        wp = game.when_played
        this_game_day = datetime.date(wp.year, wp.month, wp.day)
        if current_day != this_game_day:
            if current_day is not None:
                games_by_day.append([current_day, games_current_day])
            games_current_day = []
            current_day = this_game_day
        games_current_day.append(game)
    games_by_day.append([current_day, games_current_day])
    return render(request, 'stats_home.html', locals())

GAME_ID_RE = re.compile(r'(20[0-9]{8})gm-([0-9a-f]{4})-([0-9]{4,5})-[0-9a-f]{8}')
def api_new_game(request, game_id):
    m = GAME_ID_RE.match(game_id)
    if not m:
        return HttpResponseBadRequest('Incorrectly formatted ID')
    datehour, typeflags, lobby = m.groups()
    xmlfile = "{}/{}.xml".format(settings.TENHOU_LOG_DIR, game_id)
    if not os.path.exists(xmlfile):
        return HttpResponseBadRequest('File does not exist')
    when_tt = time.strptime(datehour, '%Y%m%d%H')
    when = datetime.datetime(
            year=when_tt.tm_year,
            month=when_tt.tm_mon,
            day=when_tt.tm_mday,
            hour=when_tt.tm_hour)
    lobby = int(lobby)
    TenhouGame(game_id=game_id, when_played=when, lobby=lobby).save()
    return HttpResponse('OK')
