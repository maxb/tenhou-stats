from django.contrib import admin

from .models import TenhouGame, TenhouPlayer

@admin.register(TenhouGame)
class TenhouGameModelAdmin(admin.ModelAdmin):
    pass

@admin.register(TenhouPlayer)
class TenhouPlayerModelAdmin(admin.ModelAdmin):
    pass
