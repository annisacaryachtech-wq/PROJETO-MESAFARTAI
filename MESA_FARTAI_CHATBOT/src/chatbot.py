import re
import unicodedata
from datetime import date, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from database import listar_ongs, listar_doadores
from doacoes_db import registrar

EXEMPLOS = {
 'doar': ['quero doar alimentos', 'tenho comida para doar', 'tenho arroz para doar amanhã', 'quero doar 15 kg de tomate hoje', 'doação de feijão', 'posso doar 40 quilos de arroz', 'tenho 20 kg de legumes', 'quero fazer uma doação'],
 'ongs': ['quais ongs recebem doações', 'mostrar ongs', 'onde estão as instituições', 'listar entidades parceiras'],
 'status': ['qual o status da minha doação', 'acompanhar doação', 'como está minha entrega'],
 'alimentos': ['quais alimentos aceitam', 'que tipos de comida posso doar', 'lista de alimentos aceitos']
}
textos = [x for grupo in EXEMPLOS.values() for x in grupo]
rotulos = [chave for chave, grupo in EXEMPLOS.items() for _ in grupo]
vetorizador = TfidfVectorizer(strip_accents='unicode', ngram_range=(1, 2))
modelo = KNeighborsClassifier(n_neighbors=3, weights='distance', metric='cosine')
modelo.fit(vetorizador.fit_transform(textos), rotulos)

def normalizar(s):
 return ''.join(c for c in unicodedata.normalize('NFKD', s.lower()) if not unicodedata.combining(c))

def extrair(texto):
 t = normalizar(texto)
 m = re.search(r'(?<!\d)(\d+(?:[.,]\d+)?)\s*(kg|kgs|quilo|quilos|quilograma|quilogramas)\b', t)
 quantidade = float(m.group(1).replace(',', '.')) if m else None
 alimentos = ['tomate', 'arroz', 'feijao', 'macarrao', 'batata', 'cenoura', 'leite', 'farinha', 'acucar', 'oleo', 'banana', 'maca', 'verdura', 'legumes', 'frutas', 'alimentos']
 alimento = next((a for a in alimentos if re.search(r'\b'+a+r's?\b', t)), None)
 if alimento:
  alimento = {'feijao':'feijão','macarrao':'macarrão','acucar':'açúcar','oleo':'óleo','maca':'maçã'}.get(alimento, alimento).capitalize()
 if 'hoje' in t: validade, urgencia = date.today().isoformat(), 'ALTA'
 elif 'amanha' in t: validade, urgencia = (date.today()+timedelta(days=1)).isoformat(), 'MÉDIA'
 else:
  dt = re.search(r'\b(\d{2})/(\d{2})/(\d{4})\b',t)
  if dt:
   try:
    dia = date(int(dt.group(3)),int(dt.group(2)),int(dt.group(1)))
    validade = dia.isoformat()
    urgencia = 'ALTA' if dia <= date.today() else ('MÉDIA' if dia == date.today()+timedelta(days=1) else 'BAIXA')
   except ValueError: validade, urgencia = None, None
  else: validade, urgencia = None, None
 return dict(alimento=alimento, quantidade_kg=quantidade, validade=validade, urgencia=urgencia)

def classificar(texto):
 t = normalizar(texto)
 if re.search(r'\b(previsao|tempo|clima|chuva|temperatura)\b', t) and not re.search(r'\b(doar|doacao|ong|alimento)\b', t):
  return 'fallback', 0.0
 v = vetorizador.transform([texto])
 if v.nnz == 0: return 'fallback', 0.0
 probs = modelo.predict_proba(v)[0]
 indice = probs.argmax()
 confianca = float(probs[indice])
 # Similaridade ao exemplo mais próximo também deve atingir um patamar mínimo.
 similaridade = float((v @ vetorizador.transform(textos).T).toarray().max())
 if confianca < .60 or similaridade < .24: return 'fallback', min(confianca, similaridade)
 return str(modelo.classes_[indice]), confianca

def ong_mais_proxima():
 ongs = listar_ongs()
 doadores = listar_doadores()
 if not ongs or not doadores: return None
 # KNN com distância haversine (coordenadas geográficas em radianos).
 import numpy as np
 pontos = np.radians([[o['latitude'], o['longitude']] for o in ongs])
 origem = np.radians([[doadores[0]['latitude'], doadores[0]['longitude']]])
 knn = NearestNeighbors(n_neighbors=1, metric='haversine').fit(pontos)
 dist, idx = knn.kneighbors(origem)
 return ongs[int(idx[0][0])], round(float(dist[0][0])*6371, 2)

def responder(texto):
 intencao, confianca = classificar(texto)
 if intencao == 'fallback':
  return 'Não entendi sua solicitação com segurança. Posso ajudar a registrar doações e consultar ONGs.', confianca, False
 if intencao == 'ongs':
  nomes = [o['nome'] for o in listar_ongs()]
  return 'ONGs parceiras: ' + (', '.join(nomes) if nomes else 'nenhuma cadastrada'), confianca, False
 if intencao == 'status': return 'Consulte o Dashboard para visualizar as doações registradas.', confianca, False
 if intencao == 'alimentos': return 'Recebemos alimentos próprios para consumo. Informe alimento, quantidade em kg e validade.', confianca, False
 dados = extrair(texto)
 if not dados['alimento'] or not dados['quantidade_kg'] or not dados['validade']:
  return 'Para registrar, informe alimento, quantidade em kg e validade (hoje, amanhã ou DD/MM/AAAA).', confianca, False
 melhor = ong_mais_proxima()
 if not melhor: return 'Não há ONG ou doador cadastrado para realizar o encaminhamento.', confianca, False
 ong, km = melhor
 id_doacao = registrar(dados['alimento'], dados['quantidade_kg'], dados['validade'], dados['urgencia'], ong['nome'])
 return (f"Doação #{id_doacao} registrada! 🍲\n\n**Alimento:** {dados['alimento']}\n\n**Quantidade:** {dados['quantidade_kg']:g} kg\n\n**Validade:** {dados['validade']}\n\n**Urgência:** {dados['urgencia']}\n\n**ONG mais próxima (KNN):** {ong['nome']} ({km} km)."), confianca, True
