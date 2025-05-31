from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Jogador, Partida, Propriedade, Transacao
from django.db import transaction
import random

def home(request):
    return render(request, 'jogo/home.html')

@login_required
def perfil(request):
    jogador, created = Jogador.objects.get_or_create(usuario=request.user)
    partidas = Partida.objects.filter(jogadores=jogador)
    return render(request, 'jogo/perfil.html', {
        'jogador': jogador,
        'partidas': partidas
    })

@login_required
def partidas(request):
    partidas_ativas = Partida.objects.filter(status='em_andamento')
    partidas_aguardando = Partida.objects.filter(status='aguardando')
    return render(request, 'jogo/partidas.html', {
        'partidas_ativas': partidas_ativas,
        'partidas_aguardando': partidas_aguardando
    })

@login_required
def criar_partida(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            partida = Partida.objects.create(
                nome=nome,
                status='aguardando'
            )
            jogador = Jogador.objects.get(usuario=request.user)
            partida.jogadores.add(jogador, through_defaults={'ordem': 1})
            messages.success(request, 'Partida criada com sucesso!')
            return redirect('jogo:partida', pk=partida.pk)
    return render(request, 'jogo/criar_partida.html')

@login_required
def partida(request, pk):
    partida = get_object_or_404(Partida, pk=pk)
    jogador = Jogador.objects.get(usuario=request.user)
    
    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == 'entrar' and partida.status == 'aguardando':
            # Pega o número atual de jogadores para definir a ordem
            ordem = partida.jogadores.count() + 1
            partida.jogadores.add(jogador, through_defaults={'ordem': ordem})
            messages.success(request, 'Você entrou na partida!')
        elif acao == 'iniciar' and partida.status == 'aguardando':
            partida.status = 'em_andamento'
            partida.jogador_atual = partida.jogadores.first()
            partida.save()
            messages.success(request, 'Partida iniciada!')
    
    # Busca todas as propriedades
    propriedades = {str(p.posicao): {
        'nome': p.nome,
        'preco': p.preco,
        'valor_aluguel': p.valor_aluguel,
        'dono': p.dono,
        'cor': p.cor
    } for p in Propriedade.objects.all()}
    
    return render(request, 'jogo/partida.html', {
        'partida': partida,
        'jogador': jogador,
        'propriedades': propriedades
    })

@login_required
def jogar(request, pk):
    partida = get_object_or_404(Partida, pk=pk)
    jogador = Jogador.objects.get(usuario=request.user)
    
    if partida.jogador_atual != jogador:
        messages.error(request, 'Não é sua vez de jogar!')
        return redirect('jogo:partida', pk=pk)
    
    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == 'jogar_dados':
            # Rola os dados (1 a 6)
            dado1 = random.randint(1, 6)
            dado2 = random.randint(1, 6)
            total = dado1 + dado2
            
            # Atualiza a posição do jogador
            jogador.posicao = (jogador.posicao + total) % 40  # 40 é o número total de casas
            jogador.save()
            
            # Verifica se passou pelo início
            if jogador.posicao < total:
                jogador.saldo += 200
                jogador.save()
                Transacao.objects.create(
                    partida=partida,
                    jogador_origem=jogador,
                    valor=200,
                    tipo='salario'
                )
                messages.success(request, f'Você passou pelo início e recebeu R$ 200!')
            
            # Busca a propriedade atual
            try:
                propriedade_atual = Propriedade.objects.get(posicao=jogador.posicao)
                if propriedade_atual.dono:
                    if propriedade_atual.dono != jogador:
                        # Paga aluguel
                        aluguel = propriedade_atual.valor_aluguel
                        jogador.saldo -= aluguel
                        propriedade_atual.dono.saldo += aluguel
                        jogador.save()
                        propriedade_atual.dono.save()
                        Transacao.objects.create(
                            partida=partida,
                            jogador_origem=jogador,
                            jogador_destino=propriedade_atual.dono,
                            propriedade=propriedade_atual,
                            valor=aluguel,
                            tipo='aluguel'
                        )
                        messages.info(request, f'Você pagou R$ {aluguel} de aluguel para {propriedade_atual.dono.usuario.username}')
            except Propriedade.DoesNotExist:
                propriedade_atual = None
            
            # Passa a vez para o próximo jogador
            jogadores = list(partida.jogadores.all())
            indice_atual = jogadores.index(jogador)
            proximo_indice = (indice_atual + 1) % len(jogadores)
            partida.jogador_atual = jogadores[proximo_indice]
            partida.save()
            
            messages.success(request, f'Você rolou {dado1} e {dado2} (total: {total})')
            return redirect('jogo:partida', pk=pk)
            
        elif acao == 'comprar':
            propriedade = get_object_or_404(Propriedade, pk=request.POST.get('propriedade_id'))
            if propriedade.dono is None and jogador.saldo >= propriedade.preco:
                with transaction.atomic():
                    jogador.saldo -= propriedade.preco
                    jogador.save()
                    propriedade.dono = jogador
                    propriedade.save()
                    Transacao.objects.create(
                        partida=partida,
                        jogador_origem=jogador,
                        propriedade=propriedade,
                        valor=propriedade.preco,
                        tipo='compra'
                    )
                messages.success(request, f'Você comprou {propriedade.nome}!')
                return redirect('jogo:partida', pk=pk)
    
    # Busca a propriedade atual para exibição
    try:
        propriedade_atual = Propriedade.objects.get(posicao=jogador.posicao)
    except Propriedade.DoesNotExist:
        propriedade_atual = None
    
    return render(request, 'jogo/jogar.html', {
        'partida': partida,
        'jogador': jogador,
        'propriedade_atual': propriedade_atual
    })

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Jogador.objects.create(usuario=user)
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'jogo/registro.html', {'form': form})
