from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render

import datetime
import os
import re
import time
from urllib.parse import urlencode

from .models import TenhouGame, TenhouPlayer, Epoch

import TenhouDecoder

def format_round(r):
    base_round, honba, riibo = r.round
    round_string = base_round + "局"
    if honba:
        round_string += " {}本場".format(honba)
    return round_string

AGARI_TYPE = {
    'RON': 'ロン',
    'TSUMO': 'ツモ',
}
def format_agari(agari, game):
    a_type = AGARI_TYPE[agari.type]
    a = "{} {}".format(game.players[agari.player].name, a_type)
    if agari.type == 'RON':
        a += " {}".format(game.players[agari.fromPlayer].name)
    a += " {}点".format(agari.points)
    if hasattr(agari, 'limit'):
        a += " {}".format(agari.limit.upper())
    a += " ("
    if hasattr(agari, 'yaku'):
        yaku = []
        for name, han in agari.yaku:
            if han == 0:
                pass
            elif name.endswith('dora'):
                yaku.append("{} {}".format(name, han))
            elif name in yaku:
                yaku[yaku.index(name)] = "dabu" + name
            else:
                yaku.append(name)
        a += ', '.join(yaku)
    if hasattr(agari, 'yakuman'):
        a += ', '.join(agari.yakuman)
    a += ")"
    return a

def stats_index(request):
    epochs = Epoch.objects.all().order_by('epoch')
    return render(request, 'stats_index.html', locals())

def stats_home(request, epoch):
    try:
        epoch_obj = Epoch.objects.get(epoch=epoch)
    except Epoch.DoesNotExist:
        raise Http404()
    players = TenhouPlayer.objects.filter(epoch=epoch).order_by('tenhou_name')
    games_by_day = []
    current_day = None
    games_current_day = None
    for game in TenhouGame.objects.filter(epoch=epoch).order_by('-when_played', '-id'):
        wp = game.when_played
        this_game_day = datetime.date(wp.year, wp.month, wp.day)
        if current_day != this_game_day:
            if current_day is not None:
                games_by_day.append([current_day, games_current_day])
            games_current_day = []
            current_day = this_game_day
        games_current_day.append(game)
        fname = "{}/{}.xml".format(settings.TENHOU_LOG_DIR, game.game_id)
        gdata = TenhouDecoder.Game()
        with open(fname, 'rb') as f:
            gdata.decode(f)
        game.nplayers = len(gdata.players)
        game.rounds = []
        for r in gdata.rounds:
            round_string = format_round(r)
            if len(r.agari) == 1:
                extra = None
                round_string += ": " + format_agari(r.agari[0], gdata)
            elif len(r.agari) == 0:
                extra = None
                if r.ryuukyoku:
                    round_string += ": 流局"
                else:
                    round_string += ": SOME KIND OF ABORTIVE DRAW?"
            else:
                extra = [format_agari(x, gdata) for x in r.agari]
            game.rounds.append((round_string, extra))
    games_by_day.append([current_day, games_current_day])
    title = epoch_obj.name
    return render(request, 'stats_home.html', locals())

GAME_ID_RE = re.compile(r'(20[0-9]{8})gm-([0-9a-f]{4})-([0-9]{4,5})-[0-9a-f]{8}')
def api_new_game(request, game_id):
    m = GAME_ID_RE.match(game_id)
    if not m:
        return HttpResponseBadRequest('Incorrectly formatted ID')
    fname = "{}/{}.xml".format(settings.TENHOU_LOG_DIR, game_id)
    if not os.path.exists(fname):
        return HttpResponseBadRequest('File does not exist')
    try:
        TenhouGame.objects.get(game_id=game_id)
        return HttpResponse('OK (already known)')
    except TenhouGame.DoesNotExist:
        pass
    process_game(game_id, m, fname)
    return HttpResponse('OK')

def process_game(game_id, m, fname, game=None):
    datehour, typeflags, lobby = m.groups()
    when_tt = time.strptime(datehour, '%Y%m%d%H')
    when = datetime.datetime(
            year=when_tt.tm_year,
            month=when_tt.tm_mon,
            day=when_tt.tm_mday,
            hour=when_tt.tm_hour)
    lobby = int(lobby)
    with open(fname, 'rb') as f:
        gdata = TenhouDecoder.Game()
        gdata.decode(f)

    full_stats = lobby == 1303 and len(gdata.players) == 4
    if lobby == 1303:
        epoch = 'lmc-season-1' if when.year < 2015 else 'lmc-season-2'
    else:
        epoch = 'adhoc'
    owari = gdata.owari.split(',')
    data = []
    urlparams = []
    for i, xmlplayer in enumerate(gdata.players):
        num = owari[i * 2 + 1]
        if num[0] != '-':
            num = "+" + num
        username = xmlplayer.name
        urlparams.append(('n{}'.format(i), username))
        if full_stats:
            try:
                dbplayer = TenhouPlayer.objects.get(epoch=epoch, tenhou_name=username)
            except TenhouPlayer.DoesNotExist:
                dbplayer = TenhouPlayer(epoch=epoch, tenhou_name=username, ndays=1)
            if dbplayer.rank_time is None or game.when_played > dbplayer.rank_time:
                dbplayer.rank_time = game.when_played
                dbplayer.rank = xmlplayer.rank
                dbplayer.rate = xmlplayer.rate
        else:
            dbplayer = None
        data.append((username, num, float(num), i, dbplayer))
    data_byplacement = data[:]
    data_byplacement.sort(key=lambda x: x[2], reverse=True)

    if game is None:
        game = TenhouGame(game_id=game_id)
    else:
        assert game_id == game.game_id
    game.epoch = epoch
    game.when_played = when
    game.lobby = lobby
    game.scores = " ".join(("{}({})".format(name, score) for name, score, _, _, _ in data_byplacement))
    game.url_names = urlencode(urlparams)
    game.save()

    if full_stats:
        for r in gdata.rounds:
            for agari in r.agari:
                if hasattr(agari, 'limit'):
                    dbplayer = data[agari.player][4]
                    setattr(dbplayer, 'n' + agari.limit,
                            getattr(dbplayer, 'n' + agari.limit) + 1)

        data_byplacement[0][4].nplace1 += 1
        data_byplacement[1][4].nplace2 += 1
        data_byplacement[2][4].nplace3 += 1
        data_byplacement[3][4].nplace4 += 1

        for _, _, _, _, dbplayer in data:
            dbplayer.ngames += 1
            if dbplayer.id:
                if not dbplayer.tenhougame_set.filter(
                        when_played__gte=when.replace(hour=0),
                        when_played__lt=when.replace(hour=0) + datetime.timedelta(days=1),
                        ).exists():
                    dbplayer.ndays += 1
            dbplayer.save()
            game.players.add(dbplayer)
