from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect

import datetime
import os
import re
import time
from urllib.parse import urlencode

from .models import TenhouGame, Epoch

from . import TenhouDecoder
from . import tenhou_fetch

def home(request):
    return redirect('/stats/')

def format_round(r):
    base_round, honba, riibo = r.round
    round_string = base_round + "局"
    if honba:
        round_string += " {}本場".format(honba)
    return round_string

RYUUKYOKU_NAMES = {
    "yao9":   'kyuushu kyuuhai',
    "reach4": 'suucha riichi',
    "ron3":   'sanchahou',
    "kan4":   'suu kaikan',
    "kaze4":  'suufon renta',
    "nm":     'nagashi mangan',
}

AGARI_TYPE = {
    'RON': 'ロン',
    'TSUMO': 'ツモ',
}
seat = '東南西北'
def format_agari(agari, game, byseat=False):
    a_type = AGARI_TYPE[agari.type]
    if byseat:
        a = "{} {}".format(seat[agari.player], a_type)
    else:
        a = "{} {}".format(game.players[agari.player].name, a_type)
    if agari.type == 'RON':
        if byseat:
            a += " {}".format(seat[agari.fromPlayer])
        else:
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

def stats_game(request, game):
    try:
        try:
            game = int(game)
            game = TenhouGame.objects.get(id=game)
        except ValueError:
            game = TenhouGame.objects.get(game_id=game)
    except TenhouGame.DoesNotExist:
        raise Http404()
    games = [game]
    decorate_for_template(game)
    title = game.game_id
    return render(request, 'stats_game.html', locals())

def markdown_escaper(x):
    return x.replace('^', r'\^')

def decorate_for_template(game, markdown_escape=False, byseat=False):
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
            round_string += ": " + format_agari(r.agari[0], gdata, byseat=byseat)
        elif len(r.agari) == 0:
            extra = None
            round_string += ": 流局"
            if r.ryuukyoku is not True:
                round_string += " {}".format(RYUUKYOKU_NAMES[r.ryuukyoku])
            if r.ryuukyoku_tenpai is not None:
                if byseat:
                    tenpai_players = [seat[x] for x in r.ryuukyoku_tenpai]
                else:
                    tenpai_players = [gdata.players[x].name for x in r.ryuukyoku_tenpai]
                round_string += " (tenpai: {})".format(", ".join(tenpai_players))
        else:
            extra = [format_agari(x, gdata) for x in r.agari]
        if markdown_escape:
            game.rounds.append((markdown_escaper(round_string), [markdown_escaper(x) for x in extra] if extra else extra))
        else:
            game.rounds.append((round_string, extra))
    if byseat:
        owari = gdata.owari.split(',')
        data = []
        for i, xmlplayer in enumerate(gdata.players):
            num = owari[i * 2 + 1]
            if num[0] != '-':
                num = "+" + num
            data.append((num, float(num), i))
        data.sort(key=lambda x: x[1], reverse=True)
        game.scores = " ".join(("{}({})".format(seat[i], score) for score, _, i in data))
    if markdown_escape:
        game.scores = markdown_escaper(game.scores)

def stats_home(request, epoch):
    if epoch.endswith("BYSEAT"):
        byseat = True
        epoch = epoch[:-6]
    else:
        byseat = False
    try:
        epoch_obj = Epoch.objects.get(epoch=epoch)
    except Epoch.DoesNotExist:
        raise Http404()
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
        decorate_for_template(game, byseat=byseat)
    games_by_day.append([current_day, games_current_day])
    title = epoch_obj.name
    return render(request, 'stats_home.html', locals())

def stats_markdown(request, epoch):
    try:
        epoch_obj = Epoch.objects.get(epoch=epoch)
    except Epoch.DoesNotExist:
        raise Http404()
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
        decorate_for_template(game, markdown_escape=True)
    games_by_day.append([current_day, games_current_day])
    return render(request, 'stats_markdown.txt', locals(), content_type='text/plain; charset=UTF-8')

BASE_URL = 'http://mahjong.maxb.eu/'
def api_new_game(request, game_id, epoch=None):
    if not tenhou_fetch.GAME_ID_RE.match(game_id):
        return HttpResponseBadRequest('Incorrectly formatted ID')

    game_id = tenhou_fetch.tenhouHash(game_id)

    fname = "{}/{}.xml".format(settings.TENHOU_LOG_DIR, game_id)
    if not os.path.exists(fname):
        tenhou_fetch.download_game(game_id, fname)

    if epoch is None:
        epoch_obj = None
    else:
        try:
            epoch_obj = Epoch.objects.get(epoch=epoch)
        except Epoch.DoesNotExist:
            epoch_obj = None

    try:
        game = TenhouGame.objects.get(game_id=game_id)
        if epoch and epoch != game.epoch and game.epoch == 'adhoc':
            process_game(game_id, fname, epoch, game)
        already = True
    except TenhouGame.DoesNotExist:
        game = process_game(game_id, fname, epoch)
        already = False

    message = "View game at {}game/{}".format(BASE_URL, game.id)
    if game.epoch != 'adhoc':
        message += ' - stats at {}stats/{}'.format(BASE_URL, game.epoch)
    if already:
        message += ' [this game was already in the database]'

    return HttpResponse(message)

GAME_ID_PARTS_RE = re.compile(r'(20[0-9]{8})gm-([0-9a-f]{4})-([0-9]{4,5})-[0-9a-f]{8}')
def process_game(game_id, fname, epoch, game=None):
    m = GAME_ID_PARTS_RE.match(game_id)
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

    if epoch is None:
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
        data.append((username, num, float(num), i))
    data_byplacement = data[:]
    data_byplacement.sort(key=lambda x: x[2], reverse=True)

    if game is None:
        game = TenhouGame(game_id=game_id)
    else:
        assert game_id == game.game_id
    game.epoch = epoch
    game.when_played = when
    game.lobby = lobby
    game.scores = " ".join(("{}({})".format(name, score) for name, score, _, _ in data_byplacement))
    game.url_names = urlencode(urlparams)
    game.save()

    return game
