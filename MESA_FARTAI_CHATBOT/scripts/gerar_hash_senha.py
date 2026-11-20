"""Gera hash PBKDF2 para configurar o acesso administrativo.
Execute: python scripts/gerar_hash_senha.py
"""
import hashlib, getpass, secrets
senha = getpass.getpass('Digite a senha administrativa: ')
if len(senha) < 10:
    raise SystemExit('Use uma senha com pelo menos 10 caracteres.')
salt = secrets.token_hex(16)
hash_senha = hashlib.pbkdf2_hmac('sha256', senha.encode(), salt.encode(), 310_000).hex()
print('
Guarde estes valores em local seguro:')
print(f'admin_salt = "{salt}"')
print(f'admin_hash = "{hash_senha}"')
print('Não compartilhe nem envie esses valores ao GitHub.')
