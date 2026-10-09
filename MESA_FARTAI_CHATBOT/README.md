# MESA FARTAI — Logística e Inteligência Assistiva

Chatbot acadêmico para apoio à logística de doações de alimentos, conectando doadores e ONGs.

## Funcionalidades
- Chat interativo com Streamlit.
- Classificação de intenções usando TF-IDF + KNN.
- Threshold de confiança: abaixo de 0,60 o chatbot responde com fallback amigável.
- Extração de entidades com RegEx: quantidade, unidade, tipo de alimento e prazo.
- Cadastro de doações em SQLite.
- Consulta de ONGs.
- Matching logístico por menor distância usando latitude/longitude.
- Registro de atendimentos e status.

## Como executar

1. Instale o Python 3.10+.
2. Abra o terminal na pasta do projeto.
3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Inicialize o banco:

```bash
python src/database.py
```

5. Execute o chatbot:

```bash
streamlit run src/app.py
```

O navegador abrirá a interface do sistema.

## Estrutura

- `src/app.py` — interface do chatbot.
- `src/database.py` — banco SQLite e dados de teste.
- `src/regex_entities.py` — extração de entidades.
- `src/matching.py` — cálculo de distância e matching.
- `data/doacoes_teste.csv` — dataset simples para teste.
- `docs/regras.txt` — regras do projeto.
- `docs/escopo_projeto.md` — escopo e prompt utilizado.
