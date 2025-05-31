# Banco Imobiliário

Um jogo de tabuleiro estilo Monopoly implementado em Django.

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário (opcional):
```bash
python manage.py createsuperuser
```

7. Execute o servidor de desenvolvimento:
```bash
python manage.py runserver
```

O projeto estará disponível em http://localhost:8000

## Estrutura do Projeto

- `banco_imobiliario/` - Configurações principais do projeto
- `jogo/` - Aplicação principal do jogo
  - `models.py` - Modelos do jogo (Jogador, Propriedade, etc.)
  - `views.py` - Lógica de apresentação
  - `templates/` - Templates HTML
  - `static/` - Arquivos estáticos (CSS, JS, imagens) 