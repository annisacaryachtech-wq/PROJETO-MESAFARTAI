import sys
from pathlib import Path
import pandas as pd
import streamlit as st
sys.path.insert(0, str(Path(__file__).resolve().parent))
from database import inicializar_banco, listar_ongs
from doacoes_db import iniciar, resumo
from chatbot import responder

st.set_page_config(page_title='MESAFARTAI', page_icon='🍲', layout='wide')
inicializar_banco()
iniciar()
base = Path(__file__).resolve().parent.parent
logo = base / 'assets' / 'logo.png'
if logo.exists(): st.sidebar.image(str(logo), width=180)
st.sidebar.title('MESAFARTAI')
st.sidebar.info('ODS 2 — Fome Zero')
st.sidebar.markdown('**Integrantes do grupo**')
st.sidebar.caption('Preencher em integrantes.txt')
integrantes = base / 'integrantes.txt'
if integrantes.exists():
 for nome in integrantes.read_text(encoding='utf-8').splitlines():
  if nome.strip() and not nome.lstrip().startswith('#'): st.sidebar.write('• ' + nome.strip())
if 'historico' not in st.session_state: st.session_state.historico = []
if st.session_state.pop('doacao_gravada', False): st.toast('Doação processada e registrada no banco!', icon='🍲')
if st.sidebar.button('🧹 Limpar Conversa'):
 st.session_state.historico = []
 st.rerun()
st.sidebar.caption('NLU: TF-IDF + KNN | Matching: KNN geográfico | Banco: SQLite')
aba_chat, aba_dash = st.tabs(['💬 Chatbot de Doações', '📊 Dashboard de Impacto Social'])
with aba_chat:
 st.title('🍲 MESAFARTAI')
 st.write('Conectando doações de alimentos a ONGs parceiras.')
 for msg in st.session_state.historico:
  with st.chat_message(msg['role']):
   st.markdown(msg['content'])
   if msg.get('confianca') is not None:
    c = msg['confianca']
    st.progress(float(c), text=f'Confiança da IA (NLU): {c*100:.1f}%')
 texto = st.chat_input('Ex.: Quero doar 15,5 kg de tomate que vencem hoje')
 if texto:
  st.session_state.historico.append({'role':'user','content':texto})
  try:
   resposta, confianca, gravou = responder(texto)
   st.session_state.historico.append({'role':'assistant','content':resposta,'confianca':confianca})
   if gravou: st.session_state.doacao_gravada = True
  except Exception as exc:
   st.session_state.historico.append({'role':'assistant','content':f'Erro ao processar: {exc}'})
  st.rerun()
with aba_dash:
 st.title('Dashboard de Impacto Social')
 total, registros = resumo()
 df = pd.DataFrame(registros, columns=['ID','Alimento','Quantidade (kg)','Validade','Urgência','ONG destino'])
 c1,c2,c3 = st.columns(3)
 c1.metric('Alimentos arrecadados', f'{total:g} kg')
 c2.metric('Doações registradas', len(df))
 c3.metric('ONGs parceiras', len(listar_ongs()))
 st.subheader('Doações reais registradas no SQLite')
 st.dataframe(df, use_container_width=True, hide_index=True)
 st.subheader('Distribuição Geográfica das ONGs')
 df_ongs = pd.DataFrame(listar_ongs())
 if not df_ongs.empty and {'latitude','longitude'}.issubset(df_ongs.columns):
  st.map(df_ongs, latitude='latitude', longitude='longitude')
 else: st.info('Nenhuma ONG com coordenadas cadastradas.')
