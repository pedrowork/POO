from django.urls import path
from . import views

app_name = 'jogo'

urlpatterns = [
    path('', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('partidas/', views.partidas, name='partidas'),
    path('partidas/criar/', views.criar_partida, name='criar_partida'),
    path('partidas/<int:pk>/', views.partida, name='partida'),
    path('partidas/<int:pk>/jogar/', views.jogar, name='jogar'),
] 