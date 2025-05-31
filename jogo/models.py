from django.db import models
from django.contrib.auth.models import User

class Propriedade(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    valor_aluguel = models.DecimalField(max_digits=10, decimal_places=2)
    posicao = models.IntegerField(unique=True)
    dono = models.ForeignKey('Jogador', on_delete=models.SET_NULL, null=True, blank=True, related_name='propriedades')
    cor = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.nome

class Jogador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=1500.00)
    posicao = models.IntegerField(default=0)
    em_jogo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.usuario.username

class Partida(models.Model):
    STATUS_CHOICES = [
        ('aguardando', 'Aguardando Jogadores'),
        ('em_andamento', 'Em Andamento'),
        ('finalizada', 'Finalizada'),
    ]
    
    nome = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aguardando')
    jogadores = models.ManyToManyField(Jogador, through='JogadorPartida')
    jogador_atual = models.ForeignKey(Jogador, on_delete=models.SET_NULL, null=True, related_name='partida_atual')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.nome

class JogadorPartida(models.Model):
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    ordem = models.IntegerField()
    
    class Meta:
        ordering = ['ordem']
        unique_together = ['jogador', 'partida']

class Transacao(models.Model):
    TIPO_CHOICES = [
        ('compra', 'Compra de Propriedade'),
        ('aluguel', 'Pagamento de Aluguel'),
        ('salario', 'Recebimento de Salário'),
        ('imposto', 'Pagamento de Imposto'),
    ]
    
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    jogador_origem = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name='transacoes_enviadas')
    jogador_destino = models.ForeignKey(Jogador, on_delete=models.SET_NULL, null=True, blank=True, related_name='transacoes_recebidas')
    propriedade = models.ForeignKey(Propriedade, on_delete=models.SET_NULL, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tipo} - {self.valor}"
