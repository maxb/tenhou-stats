from django.contrib import admin

from .models import TenhouGame, TenhouPlayer

@admin.register(TenhouGame)
class TenhouGameModelAdmin(admin.ModelAdmin):
    list_filter = ('lobby',)
    list_display = ('game_id', 'lobby', 'when_played')
    date_hierarchy = 'when_played'

@admin.register(TenhouPlayer)
class TenhouPlayerModelAdmin(admin.ModelAdmin):
    list_display = ('tenhou_name', 'rank', 'rate', 'rank_time')
