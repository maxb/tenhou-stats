from django.contrib import admin

from .models import TenhouGame, TenhouPlayer, Epoch

@admin.register(Epoch)
class EpochModelAdmin(admin.ModelAdmin):
    list_display = ('epoch', 'name',)

@admin.register(TenhouGame)
class TenhouGameModelAdmin(admin.ModelAdmin):
    list_filter = ('epoch', 'lobby',)
    list_display = ('game_id', 'epoch', 'lobby', 'when_played')
    date_hierarchy = 'when_played'

@admin.register(TenhouPlayer)
class TenhouPlayerModelAdmin(admin.ModelAdmin):
    list_display = ('epoch', 'tenhou_name', 'rank', 'rate', 'rank_time')
    list_filter = ('epoch',)
