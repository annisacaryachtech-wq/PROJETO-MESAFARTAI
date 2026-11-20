# Arquivos complementares MESAFARTAI AC-4

Este pacote adiciona arquivos que estavam ausentes na cópia conferida: datasets de referência, scripts auxiliares, exemplo de secrets, módulos auxiliares `auth.py` e `geocoding.py` e logotipo inicial.

## Importante
- Os CSVs são datasets acadêmicos de exemplo, estruturados para os campos indicados; revise-os com o professor/dataset oficial se houver um fornecido em aula.
- `secrets.toml.example` é apenas um modelo. Não contém credenciais reais. Gere o hash localmente e mantenha `secrets.toml` fora do Git.
- `auth.py` e `geocoding.py` são módulos auxiliares. A simples presença deles não ativa uma tela administrativa nem geocodificação automaticamente; a integração no fluxo existente será uma etapa posterior.
- O logotipo incluído é uma proposta gráfica inicial para `assets/logo.png`; substitua-o se o grupo possuir a marca oficial.
- O pacote não sobrescreve `app.py`, `database.py`, `chatbot.py`, banco de dados ou outros arquivos existentes.
