from django.contrib import admin
from .models import Propriedade, Jogador, Partida, JogadorPartida, Transacao

@admin.register(Propriedade)
class PropriedadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'valor_aluguel', 'posicao', 'dono', 'cor')
    list_filter = ('cor', 'dono')
    search_fields = ('nome',)

@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'saldo', 'posicao', 'em_jogo')
    list_filter = ('em_jogo',)
    search_fields = ('usuario__username',)

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'jogador_atual', 'data_criacao', 'data_fim')
    list_filter = ('status',)
    search_fields = ('nome',)

@admin.register(JogadorPartida)
class JogadorPartidaAdmin(admin.ModelAdmin):
    list_display = ('jogador', 'partida', 'ordem')
    list_filter = ('partida',)
    search_fields = ('jogador__usuario__username', 'partida__nome')

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'valor', 'jogador_origem', 'jogador_destino', 'propriedade', 'data')
    list_filter = ('tipo', 'data')
    search_fields = ('jogador_origem__usuario__username', 'jogador_destino__usuario__username')
