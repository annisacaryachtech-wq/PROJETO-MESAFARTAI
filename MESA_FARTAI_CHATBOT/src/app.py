import sys
from pathlib import Path

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

sys.path.append(str(Path(__file__).resolve().parent))

from database import (
    inicializar_banco,
    listar_ongs,
    listar_doadores,
    inserir_doacao,
    registrar_match,
    registrar_atendimento,
)
from matching import encontrar_ongs_proximas
from regex_entities import extrair_entidades

st.set_page_config(
    page_title="MESA FARTAI",
    page_icon="🍲",
    layout="centered"
)

inicializar_banco()

# Dataset pequeno e didático de intenções.
treino_textos = [
    "quero cadastrar uma doação",
    "tenho alimentos para doar",
    "quero fazer uma doação de comida",
    "quero doar alimentos",
    "tenho arroz para doar",
    "preciso encontrar uma ong",
    "quais ongs recebem doações",
    "onde posso entregar os alimentos",
    "quero consultar ongs",
    "me mostre instituições próximas",
    "qual o status da minha doação",
    "quero consultar o status",
    "minha doação já foi recebida",
    "quero saber como está a entrega",
    "quais alimentos vocês aceitam",
    "posso doar arroz",
    "posso doar feijão",
    "que tipo de alimento posso doar",
]

treino_intencoes = [
    "cadastrar_doacao",
    "cadastrar_doacao",
    "cadastrar_doacao",
    "cadastrar_doacao",
    "cadastrar_doacao",
    "consultar_ongs",
    "consultar_ongs",
    "consultar_ongs",
    "consultar_ongs",
    "consultar_ongs",
    "consultar_status",
    "consultar_status",
    "consultar_status",
    "consultar_status",
    "consultar_alimentos",
    "consultar_alimentos",
    "consultar_alimentos",
    "consultar_alimentos",
]

vectorizer = TfidfVectorizer(lowercase=True, strip_accents="unicode")
X = vectorizer.fit_transform(treino_textos)

modelo = KNeighborsClassifier(
    n_neighbors=3,
    weights="distance"
)
modelo.fit(X, treino_intencoes)


def classificar_intencao(texto):
    vetor = vectorizer.transform([texto])

    probabilidades = modelo.predict_proba(vetor)[0]
    classes = modelo.classes_

    indice = probabilidades.argmax()
    intencao = classes[indice]
    confianca = float(probabilidades[indice])

    if confianca < 0.60:
        return "fallback", confianca

    return intencao, confianca


def resposta_ongs():
    ongs = listar_ongs()

    if not ongs:
        return "Ainda não há ONGs cadastradas."

    texto = "Estas são as ONGs cadastradas:\n\n"
    for ong in ongs:
        texto += f"- **{ong['nome']}** — CEP {ong['cep']} — Tel. {ong['telefone']}\n"

    return texto


def resposta_alimentos():
    return (
        "No protótipo, trabalhamos com alimentos como arroz, feijão, leite, "
        "macarrão, óleo, açúcar, farinha e cestas básicas. "
        "Você pode informar a quantidade e o prazo na mensagem."
    )


def resposta_status():
    return (
        "O protótipo registra a doação como **DISPONÍVEL** após o cadastro. "
        "O acompanhamento completo pode ser ampliado em uma próxima versão."
    )


def processar_mensagem(mensagem):
    intencao, confianca = classificar_intencao(mensagem)
    entidades = extrair_entidades(mensagem)

    if intencao == "fallback":
        resposta = (
            "Desculpe, não consegui entender com segurança. 😕\n\n"
            "Posso ajudar com:\n"
            "- cadastro de doação;\n"
            "- consulta de ONGs;\n"
            "- consulta de status;\n"
            "- informações sobre alimentos."
        )
        registrar_atendimento(mensagem, intencao, confianca, resposta)
        return resposta, entidades, confianca

    if intencao == "consultar_ongs":
        resposta = resposta_ongs()
        registrar_atendimento(mensagem, intencao, confianca, resposta)
        return resposta, entidades, confianca

    if intencao == "consultar_alimentos":
        resposta = resposta_alimentos()
        registrar_atendimento(mensagem, intencao, confianca, resposta)
        return resposta, entidades, confianca

    if intencao == "consultar_status":
        resposta = resposta_status()
        registrar_atendimento(mensagem, intencao, confianca, resposta)
        return resposta, entidades, confianca

    if intencao == "cadastrar_doacao":
        faltando = []

        if entidades["quantidade"] is None:
            faltando.append("quantidade (ex.: 10 kg)")
        if entidades["unidade"] is None:
            faltando.append("unidade (kg, caixas, unidades...)")
        if entidades["alimento"] is None:
            faltando.append("alimento (ex.: arroz)")

        if faltando:
            resposta = (
                "Consigo cadastrar sua doação! 💚\n\n"
                "Só preciso de: **" + ", ".join(faltando) + "**.\n\n"
                "Exemplo: `Quero doar 10 kg de arroz para hoje.`"
            )
            registrar_atendimento(mensagem, intencao, confianca, resposta)
            return resposta, entidades, confianca

        doadores = listar_doadores()
        doador = doadores[0]

        doacao_id = inserir_doacao(
            doador["id"],
            entidades["alimento"],
            entidades["quantidade"],
            entidades["unidade"],
            entidades["prazo"]
        )

        ongs = listar_ongs()
        proximas = encontrar_ongs_proximas(
            doador["latitude"],
            doador["longitude"],
            ongs
        )

        melhor = proximas[0]

        registrar_match(
            doacao_id,
            melhor["id"],
            melhor["distancia_km"]
        )

        resposta = (
            f"Doação cadastrada com sucesso! ✅\n\n"
            f"**Alimento:** {entidades['alimento']}\n"
            f"**Quantidade:** {entidades['quantidade']} {entidades['unidade']}\n"
            f"**Prazo:** {entidades['prazo'] or 'não informado'}\n\n"
            f"📍 ONG sugerida pelo matching: **{melhor['nome']}** "
            f"({melhor['distancia_km']} km aproximadamente)."
        )

        registrar_atendimento(mensagem, intencao, confianca, resposta)
        return resposta, entidades, confianca


st.title("🍲 MESA FARTAI")
st.subheader("Logística e Inteligência Assistiva no Combate à Fome")
st.caption("Protótipo acadêmico — chatbot de apoio a doações de alimentos")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {
            "role": "assistant",
            "content": (
                "Olá! 👋 Sou o chatbot MESA FARTAI.\n\n"
                "Posso cadastrar doações, consultar ONGs e explicar quais "
                "alimentos podem ser doados."
            )
        }
    ]

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

pergunta = st.chat_input("Digite sua mensagem...")

if pergunta:
    st.session_state.mensagens.append({
        "role": "user",
        "content": pergunta
    })

    resposta, entidades, confianca = processar_mensagem(pergunta)

    st.session_state.mensagens.append({
        "role": "assistant",
        "content": resposta
    })

    st.rerun()

with st.sidebar:
    st.header("📌 Testes rápidos")
    st.write("Experimente:")

    exemplos = [
        "Quero doar 10 kg de arroz hoje",
        "Quais ONGs recebem doações?",
        "Posso doar feijão?",
        "Qual o status da minha doação?",
        "Olá, como você está?"
    ]

    for exemplo in exemplos:
        st.code(exemplo)

    st.divider()
    st.write("**Threshold:** 0,60")
    st.write("**IA:** TF-IDF + KNN")
    st.write("**Banco:** SQLite")
    st.write("**Extração:** RegEx")
