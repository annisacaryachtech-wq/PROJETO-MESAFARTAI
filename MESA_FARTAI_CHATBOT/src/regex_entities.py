import re

ALIMENTOS = [
    "arroz", "feijão", "feijao", "leite", "macarrão", "macarrao",
    "cesta básica", "cesta basica", "cestas básicas", "cestas basicas",
    "óleo", "oleo", "açúcar", "acucar", "farinha", "alimento", "alimentos"
]

def extrair_entidades(texto):
    texto_lower = texto.lower()

    quantidade = None
    unidade = None

    padroes = [
        r"(\d+(?:[.,]\d+)?)\s*(kg|quilo|quilos|caixa|caixas|unidade|unidades|cesta|cestas|litro|litros|l)\b",
    ]

    for padrao in padroes:
        match = re.search(padrao, texto_lower)
        if match:
            quantidade = float(match.group(1).replace(",", "."))
            unidade = match.group(2)
            break

    alimento = None
    for item in ALIMENTOS:
        if item in texto_lower:
            alimento = item
            break

    prazo = None

    hora = re.search(r"\b(\d{1,2})(?:[:h](\d{2}))?\s*h?\b", texto_lower)
    if hora and int(hora.group(1)) <= 23:
        h = hora.group(1)
        m = hora.group(2) or "00"
        prazo = f"{h.zfill(2)}:{m}"

    if "amanhã" in texto_lower or "amanha" in texto_lower:
        prazo = "amanhã"

    if "hoje" in texto_lower:
        prazo = "hoje"

    return {
        "quantidade": quantidade,
        "unidade": unidade,
        "alimento": alimento,
        "prazo": prazo
    }
