# Escopo do Projeto

## Título
MESA FARTAI — Logística e Inteligência Assistiva no Combate à Fome

## Problema
Facilitar o contato entre pessoas que possuem alimentos para doar e organizações que podem receber essas doações.

## Público-alvo
- Doadores.
- ONGs e instituições sociais.
- Equipe responsável pela logística das doações.

## Objetivos de Desenvolvimento Sustentável
O projeto se relaciona principalmente ao ODS 2 — Fome Zero e Agricultura Sustentável.

## Intenções do chatbot
- Cadastrar doação.
- Consultar ONGs.
- Consultar status.
- Solicitar informações sobre alimentos.
- Fallback para mensagens fora do escopo.

## Dados coletados
- Tipo de alimento.
- Quantidade.
- Unidade.
- Prazo/horário de validade ou disponibilidade.

## Inteligência Artificial
A classificação das mensagens utiliza:
1. TF-IDF para transformar texto em números.
2. KNN para identificar a intenção mais próxima.
3. Threshold de 0,60 para decidir quando utilizar fallback.

## Extração de entidades
Expressões regulares identificam:
- quantidade: 10 kg, 5 caixas, 20 unidades etc.
- alimento: arroz, feijão, leite, cesta etc.
- prazo: hoje, amanhã, 18h etc.

## Matching
Após o cadastro, o sistema calcula a distância aproximada entre o doador e as ONGs cadastradas e apresenta as opções mais próximas.

## Prompt utilizado como apoio à IA
"Crie um chatbot acadêmico chamado MESA FARTAI para apoiar a logística de doações de alimentos. O sistema deve cadastrar doações, consultar ONGs, extrair quantidade/unidade/tipo/prazo da mensagem, classificar intenções com TF-IDF + KNN e utilizar fallback quando a confiança for inferior a 0,60. Os dados devem ser persistidos em SQLite e o matching deve considerar a distância entre doador e ONG."
