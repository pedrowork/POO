from django import template
import hashlib

register = template.Library()

@register.filter
def hash_color(value):
    """Gera uma cor baseada no valor do input"""
    if not value:
        return '#000000'

    # Gera um hash do valor
    hash_object = hashlib.md5(str(value).encode())
    hash_hex = hash_object.hexdigest()

    # Usa os primeiros 6 caracteres do hash como cor
    return f'#{hash_hex[:6]}'

@register.filter
def get_item(dictionary, key):
    """Retorna um item de um dicionário usando a chave"""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def get_range(value, arg):
    """Retorna um range de value até arg (exclusivo)"""
    return range(int(value), int(arg))
