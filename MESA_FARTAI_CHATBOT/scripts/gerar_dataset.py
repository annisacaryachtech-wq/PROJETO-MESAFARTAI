"""Valida e resume os datasets CSV do projeto."""
from pathlib import Path
import csv
BASE = Path(__file__).resolve().parents[1] / 'data'
for nome, colunas in {
    'alimentos.csv': {'alimento','categoria','unidade_padrao','aceito'},
    'dataset_intencoes.csv': {'texto','intencao'},
    'dataset_teste.csv': {'texto','intencao_esperada'},
}.items():
    caminho = BASE / nome
    if not caminho.exists():
        raise SystemExit(f'Arquivo ausente: {caminho}')
    with caminho.open(encoding='utf-8-sig', newline='') as arquivo:
        leitor = csv.DictReader(arquivo)
        faltantes = colunas - set(leitor.fieldnames or [])
        if faltantes:
            raise SystemExit(f'{nome}: colunas ausentes: {sorted(faltantes)}')
        linhas = list(leitor)
        print(f'{nome}: {len(linhas)} registros — OK')
