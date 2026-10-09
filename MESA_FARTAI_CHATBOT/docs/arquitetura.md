# Arquitetura do Software

```text
USUÁRIO
   |
   v
STREAMLIT (Front-End)
   |
   v
CLASSIFICAÇÃO DE INTENÇÃO
TF-IDF + KNN
   |
   +---- confiança < 0,60 ---> FALLBACK
   |
   v
EXTRAÇÃO DE ENTIDADES
RegEx
   |
   v
SQLITE
   |
   v
MATCHING KNN / DISTÂNCIA
   |
   v
ONG MAIS PRÓXIMA
   |
   v
RESPOSTA / TICKET DE DOAÇÃO
```

## Camadas
- Interface: Streamlit.
- Inteligência: TF-IDF + KNN.
- Extração: RegEx.
- Persistência: SQLite.
- Matching: cálculo de distância geográfica.
