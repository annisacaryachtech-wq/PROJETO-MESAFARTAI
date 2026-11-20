# MESAFARTAI — AC-4

## Instalação no Windows / VS Code

Abra a pasta `MESA_FARTAI_CHATBOT` no VS Code. Para instalar o pacote AC-4 em uma cópia existente do projeto, extraia o ZIP em outra pasta e execute no PowerShell:

```powershell
& "C:\CAMINHO\DO\PACOTE\MESA_FARTAI_CHATBOT\instalar_ac4.ps1" -Destino (Get-Location).Path
```

Se abriu diretamente o projeto atualizado do ZIP, não precisa copiar nada. Instale e execute:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run src/app.py
```

## Teste manual

1. Envie `Quero doar 15,5 kg de tomate que vencem hoje`.
2. Envie `Tenho 40 quilos de arroz para doar amanhã`.
3. Envie `Qual a previsão do tempo hoje?` (fallback sem gravação).
4. Veja 55,5 kg, 2 registros e mapa no Dashboard (partindo de banco AC-4 vazio).
5. O botão Limpar Conversa limpa somente o histórico do chat, não as doações.

## Observações

- O projeto original possui `mesafartai.db` com uma tabela `doacoes` de esquema diferente. Para **não destruir dados antigos**, a AC-4 usa `mesafartai_ac4.db` com a tabela `doacoes` e as seis colunas solicitadas.
- O projeto original não incluía `assets/logo.png`. Adicione seu logo real nesse caminho para exibi-lo.
- Preencha `integrantes.txt` com um nome por linha.
- Os testes automatizados não substituem a validação visual no navegador.
- Para publicar no GitHub, depois de testar: `git status`, `git add .`, `git commit -m "Conclusão projeto MESAFARTAI"`, `git push origin main`.
