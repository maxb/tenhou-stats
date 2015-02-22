from django.contrib import admin

from .models import TenhouGame, TenhouPlayer

@admin.register(TenhouGame)
class TenhouGameModelAdmin(admin.ModelAdmin):
    list_filter = ('lobby',)
    list_display = ('game_id', 'lobby', 'date_played')
    date_hierarchy = 'date_played'

@admin.register(TenhouPlayer)
class TenhouPlayerModelAdmin(admin.ModelAdmin):
    pass
