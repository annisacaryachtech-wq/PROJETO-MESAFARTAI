"""Autenticação administrativa opcional via st.secrets.
Não cria credenciais padrão. Configure .streamlit/secrets.toml localmente.
"""
import hashlib
import hmac

def verificar_senha(senha: str, salt: str, hash_esperado: str) -> bool:
    if not senha or not salt or not hash_esperado:
        return False
    calculado = hashlib.pbkdf2_hmac('sha256', senha.encode(), salt.encode(), 310_000).hex()
    return hmac.compare_digest(calculado, hash_esperado)

def autenticar_streamlit(st):
    """Retorna True se autenticado; solicita senha quando secrets existem."""
    try:
        cfg = st.secrets['admin']
        salt, esperado = cfg['admin_salt'], cfg['admin_hash']
    except Exception:
        st.warning('Acesso administrativo não configurado. Consulte .streamlit/secrets.toml.example.')
        return False
    senha = st.text_input('Senha administrativa', type='password')
    if st.button('Entrar no administrador'):
        st.session_state['admin_autenticado'] = verificar_senha(senha, salt, esperado)
    return bool(st.session_state.get('admin_autenticado', False))
