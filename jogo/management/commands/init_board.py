from django.core.management.base import BaseCommand
from jogo.models import Propriedade

class Command(BaseCommand):
    help = 'Inicializa o tabuleiro com as propriedades do Banco Imobiliário'

    def handle(self, *args, **kwargs):
        propriedades = [
            # Propriedades marrons
            {'nome': 'Av. Barão de Tefé', 'preco': 60, 'valor_aluguel': 2, 'posicao': 1, 'cor': 'marrom'},
            {'nome': 'Av. Visconde de Niterói', 'preco': 60, 'valor_aluguel': 4, 'posicao': 3, 'cor': 'marrom'},
            
            # Propriedades azul claro
            {'nome': 'Av. Presidente Vargas', 'preco': 100, 'valor_aluguel': 6, 'posicao': 6, 'cor': 'azul-claro'},
            {'nome': 'Av. Rio Branco', 'preco': 100, 'valor_aluguel': 6, 'posicao': 8, 'cor': 'azul-claro'},
            {'nome': 'Rua da Quitanda', 'preco': 120, 'valor_aluguel': 8, 'posicao': 9, 'cor': 'azul-claro'},
            
            # Propriedades rosa
            {'nome': 'Av. Nossa Senhora de Copacabana', 'preco': 140, 'valor_aluguel': 10, 'posicao': 11, 'cor': 'rosa'},
            {'nome': 'Av. Vieira Souto', 'preco': 140, 'valor_aluguel': 10, 'posicao': 13, 'cor': 'rosa'},
            {'nome': 'Av. Atlântica', 'preco': 160, 'valor_aluguel': 12, 'posicao': 14, 'cor': 'rosa'},
            
            # Propriedades laranja
            {'nome': 'Av. Paulista', 'preco': 180, 'valor_aluguel': 14, 'posicao': 16, 'cor': 'laranja'},
            {'nome': 'Av. Brigadeiro Faria Lima', 'preco': 180, 'valor_aluguel': 14, 'posicao': 18, 'cor': 'laranja'},
            {'nome': 'Av. Rebouças', 'preco': 200, 'valor_aluguel': 16, 'posicao': 19, 'cor': 'laranja'},
            
            # Propriedades vermelhas
            {'nome': 'Av. Brigadeiro Luís Antônio', 'preco': 220, 'valor_aluguel': 18, 'posicao': 21, 'cor': 'vermelho'},
            {'nome': 'Av. 9 de Julho', 'preco': 220, 'valor_aluguel': 18, 'posicao': 23, 'cor': 'vermelho'},
            {'nome': 'Av. São João', 'preco': 240, 'valor_aluguel': 20, 'posicao': 24, 'cor': 'vermelho'},
            
            # Propriedades amarelas
            {'nome': 'Av. Ipiranga', 'preco': 260, 'valor_aluguel': 22, 'posicao': 26, 'cor': 'amarelo'},
            {'nome': 'Av. São Luís', 'preco': 260, 'valor_aluguel': 22, 'posicao': 27, 'cor': 'amarelo'},
            {'nome': 'Rua Augusta', 'preco': 280, 'valor_aluguel': 24, 'posicao': 29, 'cor': 'amarelo'},
            
            # Propriedades verdes
            {'nome': 'Av. Berrini', 'preco': 300, 'valor_aluguel': 26, 'posicao': 31, 'cor': 'verde'},
            {'nome': 'Av. Morumbi', 'preco': 300, 'valor_aluguel': 26, 'posicao': 32, 'cor': 'verde'},
            {'nome': 'Av. Faria Lima', 'preco': 320, 'valor_aluguel': 28, 'posicao': 34, 'cor': 'verde'},
            
            # Propriedades azul escuro
            {'nome': 'Av. Presidente Juscelino Kubitschek', 'preco': 350, 'valor_aluguel': 35, 'posicao': 37, 'cor': 'azul-escuro'},
            {'nome': 'Av. Paulista', 'preco': 400, 'valor_aluguel': 50, 'posicao': 39, 'cor': 'azul-escuro'},
        ]

        for prop in propriedades:
            Propriedade.objects.get_or_create(
                nome=prop['nome'],
                defaults={
                    'preco': prop['preco'],
                    'valor_aluguel': prop['valor_aluguel'],
                    'posicao': prop['posicao'],
                    'cor': prop['cor']
                }
            )

        self.stdout.write(self.style.SUCCESS('Tabuleiro inicializado com sucesso!')) 