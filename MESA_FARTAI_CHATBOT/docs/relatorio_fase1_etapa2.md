# Relatório Fase 1 - Etapa 2

## 1. Quantas árvores foram utilizadas?

O modelo Random Forest foi configurado com 80 árvores.

## 2. Qual foi o threshold utilizado?

Foi utilizado um threshold de 0.60, ou seja, 60% de confiança.

Quando a confiança fica abaixo de 60%, o sistema retorna fallback.

## 3. Resultado da primeira execução

Foram realizados testes com quatro frases:

- "Tenho 30 kg de banana para doar" → cadastrar_doacao
- "Nossa instituição precisa de mantimentos" → fallback
- "Qual é a receita de bolo de cenoura?" → fallback
- "coisa comida doar la" → fallback

A frase relacionada à doação foi identificada corretamente.

As frases com menor confiança foram direcionadas para o fallback.

## 4. Como melhorar a confiança?

A confiança pode ser melhorada adicionando mais frases de treinamento, principalmente frases diferentes que representem a mesma intenção.

Também podem ser adicionados:

- Variações de escrita;
- Erros de digitação;
- Diferentes formas de fazer uma solicitação;
- Mais exemplos de cada intenção;
- Dados de treinamento mais equilibrados;
- Ajustes no número de árvores do Random Forest;
- Testes com diferentes valores de threshold.

## 5. Por que o Random Forest foi escolhido?

O Random Forest foi escolhido porque combina várias árvores de decisão, aumentando a estabilidade da classificação.

Ele também funciona bem com os dados transformados pelo TF-IDF e permite obter probabilidades de confiança para cada classificação.

Isso possibilita utilizar o threshold de 60% e enviar mensagens com baixa confiança para o fallback.
