from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier


# Frases de treinamento
frases = [
    "Tenho alimentos para doar",
    "Quero doar comida",
    "Tenho 30 kg de banana para doar",
    "Gostaria de cadastrar uma doação",
    "Quero cadastrar minha doação",
    "Tenho alimentos disponíveis",

    "Preciso de alimentos",
    "Minha instituição precisa de comida",
    "Nossa ONG precisa de mantimentos",
    "Precisamos receber doações",
    "Quero solicitar uma doação",
    "Minha instituição precisa de alimentos",

    "Olá",
    "Oi",
    "Bom dia",
    "Boa tarde",
    "Boa noite",

    "Qual é a receita de bolo?",
    "Quem é o presidente?",
    "Como está o tempo?",
    "Quero saber sobre futebol",
]

# Classes correspondentes às frases
intencoes = [
    "cadastrar_doacao",
    "cadastrar_doacao",
    "cadastrar_doacao",
    "cadastrar_doacao",
    "cadastrar_doacao",
    "cadastrar_doacao",

    "solicitar_doacao",
    "solicitar_doacao",
    "solicitar_doacao",
    "solicitar_doacao",
    "solicitar_doacao",
    "solicitar_doacao",

    "saudacao",
    "saudacao",
    "saudacao",
    "saudacao",

    "fora_de_escopo",
    "fora_de_escopo",
    "fora_de_escopo",
    "fora_de_escopo",
]


# Criação do vetorizador TF-IDF
vetorizador = TfidfVectorizer(
    ngram_range=(1, 2)
)

X = vetorizador.fit_transform(frases)


# Criação do modelo Random Forest
modelo = RandomForestClassifier(
    n_estimators=80,
    random_state=42
)

modelo.fit(X, intencoes)


class MotorNLU:

    def __init__(self, limiar_threshold=0.60):
        self.limiar_threshold = limiar_threshold

    def classificar(self, texto):

        # Transforma o texto recebido em vetor
        vetor = vetorizador.transform([texto])

        # Descobre as probabilidades de cada intenção
        probabilidades = modelo.predict_proba(vetor)[0]

        # Pega a maior probabilidade
        maior_indice = probabilidades.argmax()
        confianca = probabilidades[maior_indice]

        # Descobre a intenção prevista
        intencao = modelo.classes_[maior_indice]

        # Aplica a trava de threshold
        if confianca < self.limiar_threshold:
            return "fallback", confianca

        # Fora de escopo também deve gerar fallback
        if intencao == "fora_de_escopo":
            return "fallback", confianca

        return intencao, confianca

    def responder(self, texto):

        intencao, confianca = self.classificar(texto)

        if intencao == "fallback":
            return (
                "Desculpe, não consegui entender com clareza o seu pedido.\n"
                "Você pode refazer a mensagem informando se deseja "
                "**doar alimentos** ou **solicitar doações para uma ONG**?"
            )

        return (
            f"Intenção '{intencao}' identificada "
            f"com {confianca:.1%} de confiança."
        )


# Testes
if __name__ == "__main__":

    motor = MotorNLU(limiar_threshold=0.60)

    testes = [
        "Tenho 30 kg de banana para doar",
        "Nossa instituição precisa de mantimentos",
        "Qual é a receita de bolo de cenoura?",
        "coisa comida doar la",
    ]

    print(
        "[NLU] Modelo Random Forest e Vetorizador "
        "TF-IDF treinados com sucesso!"
    )

    print("\n--- BATERIA DE TESTES DE ESTRESSE NLU ---")

    for frase in testes:

        intencao, confianca = motor.classificar(frase)

        print(f"\nEntrada: '{frase}'")
        print(
            f"Intenção: {intencao} | "
            f"Confiança: {confianca:.2f}"
        )

        print(f"Retorno: {motor.responder(frase)}")
