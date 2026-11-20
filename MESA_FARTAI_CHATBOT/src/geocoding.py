"""Geocodificação opcional via serviço Nominatim (OpenStreetMap).
Respeite os limites de uso e informe um user-agent identificável.
"""
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

def geocodificar(endereco: str, user_agent: str, timeout: int = 10):
    if not endereco.strip() or not user_agent.strip():
        raise ValueError('Informe endereço e user-agent identificável.')
    url = 'https://nominatim.openstreetmap.org/search?' + urlencode({'q': endereco, 'format': 'jsonv2', 'limit': 1})
    req = Request(url, headers={'User-Agent': user_agent})
    with urlopen(req, timeout=timeout) as resposta:
        dados = json.loads(resposta.read().decode('utf-8'))
    if not dados:
        return None
    return {'latitude': float(dados[0]['lat']), 'longitude': float(dados[0]['lon']), 'display_name': dados[0].get('display_name','')}
