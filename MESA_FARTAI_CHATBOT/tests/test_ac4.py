import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import chatbot
import doacoes_db
from database import inicializar_banco

def test_entidades():
 d = chatbot.extrair('Quero doar 15,5 kg de tomate que vencem hoje')
 assert d['alimento'] == 'Tomate' and d['quantidade_kg'] == 15.5 and d['urgencia'] == 'ALTA'
 d = chatbot.extrair('Tenho 40 quilos de arroz para doar amanhã')
 assert d['alimento'] == 'Arroz' and d['quantidade_kg'] == 40 and d['urgencia'] == 'MÉDIA'

def test_fallback():
 assert chatbot.classificar('Qual a previsão do tempo hoje?')[0] == 'fallback'

def test_integracao(tmp_path, monkeypatch):
 inicializar_banco()
 monkeypatch.setattr(doacoes_db, 'CAMINHO', tmp_path / 'teste.db')
 doacoes_db.iniciar()
 a = chatbot.responder('Quero doar 15,5 kg de tomate que vencem hoje')
 b = chatbot.responder('Tenho 40 quilos de arroz para doar amanhã')
 c = chatbot.responder('Qual a previsão do tempo hoje?')
 total, linhas = doacoes_db.resumo()
 assert a[2] and b[2] and not c[2]
 assert total == 55.5 and len(linhas) == 2
 assert {linha[4] for linha in linhas} == {'ALTA', 'MÉDIA'}
