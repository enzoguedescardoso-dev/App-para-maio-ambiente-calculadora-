import json

from flask import Flask, request, render_template

app = Flask(__name__)

CATEGORIAS = [
    {
        "chave": "carro", "icone": "🚗", "rotulo": "Transporte de carro",
        "pergunta": "Quantas vezes você usa carro por semana?",
        "unidade": "vez(es) por semana",
        "peso": 3, "bonus": False, "min": 0, "max": 20, "padrao": 3,
        "limite_alto": 10, "limite_medio": 4,
        "texto_alto": "seu resultado é péssimo nisso, troque parte dos seus trajetos por bicicleta, caminhada ou transporte público. Caso não faça isso, a poluição do ar e o aquecimento global vão continuar piorando!!!",
        "texto_medio": "seu resultado é mediano nisso, tente trocar mais uma ou duas viagens de carro por semana por alternativas sustentáveis. Caso não faça isso, seu impacto no trânsito e na poluição vai continuar crescendo!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue priorizando bicicleta, caminhada ou transporte público. Caso comece a usar mais o carro, sua pegada de carbono vai disparar rapidamente!!!",
    },
    {
        "chave": "luz", "icone": "💡", "rotulo": "Iluminação em casa",
        "pergunta": "Quantas horas por dia as luzes da sua casa ficam ligadas?",
        "unidade": "hora(s) por dia",
        "peso": 2, "bonus": False, "min": 0, "max": 24, "padrao": 4,
        "limite_alto": 8, "limite_medio": 4,
        "texto_alto": "seu resultado é péssimo nisso, apague mais as luzes ao seu redor. Caso não faça isso, a energia do mundo poderá acabar!!!",
        "texto_medio": "seu resultado é mediano nisso, aproveite mais a luz natural durante o dia e apague ambientes vazios. Caso não faça isso, seu consumo de energia vai continuar alto!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue economizando energia. Caso volte a deixar luzes acesas à toa, o consumo de energia vai disparar!!!",
    },
    {
        "chave": "carne", "icone": "🥩", "rotulo": "Consumo de carne",
        "pergunta": "Quantas refeições com carne você faz por semana?",
        "unidade": "refeição(ões) por semana",
        "peso": 2, "bonus": False, "min": 0, "max": 21, "padrao": 5,
        "limite_alto": 10, "limite_medio": 5,
        "texto_alto": "seu resultado é péssimo nisso, reduza o consumo de carne vermelha e inclua dias vegetarianos na semana. Caso não faça isso, o desmatamento e as emissões de metano vão continuar aumentando!!!",
        "texto_medio": "seu resultado é mediano nisso, tente substituir algumas refeições por opções vegetais ou frango. Caso não faça isso, a pecuária vai continuar pressionando os recursos naturais!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue com uma alimentação equilibrada. Caso aumente muito o consumo de carne, seu impacto ambiental vai crescer bastante!!!",
    },
    {
        "chave": "banho", "icone": "🚿", "rotulo": "Tempo de banho",
        "pergunta": "Quantos minutos você fica no banho, em média, por dia?",
        "unidade": "minuto(s) por dia",
        "peso": 1, "bonus": False, "min": 0, "max": 60, "padrao": 8,
        "limite_alto": 20, "limite_medio": 10,
        "texto_alto": "seu resultado é péssimo nisso, reduza o tempo do banho para economizar água. Caso não faça isso, os reservatórios de água doce vão continuar sendo esgotados!!!",
        "texto_medio": "seu resultado é mediano nisso, tente diminuir alguns minutos do banho. Caso não faça isso, o consumo de água tratada vai continuar alto!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue economizando água no banho. Caso aumente muito o tempo, o desperdício de água vai crescer rápido!!!",
    },
    {
        "chave": "plastico", "icone": "🥤", "rotulo": "Plástico descartável",
        "pergunta": "Quantos itens de plástico descartável (copos, sacolas, talheres) você usa por semana?",
        "unidade": "item(ns) por semana",
        "peso": 2, "bonus": False, "min": 0, "max": 30, "padrao": 5,
        "limite_alto": 15, "limite_medio": 5,
        "texto_alto": "seu resultado é péssimo nisso, troque por opções reutilizáveis o quanto antes. Caso não faça isso, os oceanos vão continuar se enchendo de plástico!!!",
        "texto_medio": "seu resultado é mediano nisso, tente reduzir aos poucos o uso de descartáveis. Caso não faça isso, a poluição plástica vai continuar aumentando!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue evitando plásticos descartáveis. Caso volte a usar muito, a poluição dos mares vai voltar a crescer!!!",
    },
    {
        "chave": "roupas", "icone": "👕", "rotulo": "Compra de roupas",
        "pergunta": "Quantas peças de roupa novas você compra por mês?",
        "unidade": "peça(s) por mês",
        "peso": 4, "bonus": False, "min": 0, "max": 20, "padrao": 2,
        "limite_alto": 8, "limite_medio": 3,
        "texto_alto": "seu resultado é péssimo nisso, a indústria da moda rápida é uma das que mais poluem o planeta. Caso não reduza, o consumo de água e recursos têxteis vai continuar disparando!!!",
        "texto_medio": "seu resultado é mediano nisso, tente comprar roupas de segunda mão ou de marcas sustentáveis. Caso não faça isso, seu impacto têxtil vai continuar crescendo!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue consumindo moda de forma consciente. Caso volte a comprar em excesso, os recursos naturais vão continuar sendo consumidos rapidamente!!!",
    },
    {
        "chave": "desperdicio", "icone": "🍽️", "rotulo": "Desperdício de comida",
        "pergunta": "Quantas vezes por semana você joga comida fora?",
        "unidade": "vez(es) por semana",
        "peso": 3, "bonus": False, "min": 0, "max": 14, "padrao": 1,
        "limite_alto": 5, "limite_medio": 2,
        "texto_alto": "seu resultado é péssimo nisso, planeje melhor suas compras e reaproveite as sobras. Caso não faça isso, o desperdício de recursos e alimentos vai continuar aumentando!!!",
        "texto_medio": "seu resultado é mediano nisso, tente aproveitar melhor os alimentos antes de descartá-los. Caso não faça isso, o lixo orgânico vai continuar gerando gases de efeito estufa em aterros!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue aproveitando bem os alimentos. Caso comece a desperdiçar mais, o impacto ambiental do lixo orgânico vai aumentar rapidamente!!!",
    },
    {
        "chave": "arcondicionado", "icone": "❄️", "rotulo": "Ar-condicionado / aquecedor",
        "pergunta": "Quantas horas por dia você usa ar-condicionado ou aquecedor?",
        "unidade": "hora(s) por dia",
        "peso": 2, "bonus": False, "min": 0, "max": 24, "padrao": 2,
        "limite_alto": 8, "limite_medio": 3,
        "texto_alto": "seu resultado é péssimo nisso, tente usar ventilação natural e roupas adequadas ao clima. Caso não faça isso, o consumo de energia elétrica vai continuar disparando!!!",
        "texto_medio": "seu resultado é mediano nisso, reduza algumas horas de uso por dia. Caso não faça isso, sua conta de luz e o impacto ambiental vão continuar altos!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue controlando o uso de climatização. Caso aumente muito o uso, o consumo de energia vai crescer rapidamente!!!",
    },
    {
        "chave": "voos", "icone": "✈️", "rotulo": "Viagens de avião",
        "pergunta": "Quantas viagens de avião você faz por ano?",
        "unidade": "viagem(ns) por ano",
        "peso": 10, "bonus": False, "min": 0, "max": 10, "padrao": 0,
        "limite_alto": 4, "limite_medio": 1,
        "texto_alto": "seu resultado é péssimo nisso, voos são uma das maiores fontes de emissão de carbono por pessoa. Caso não reduza, sua pegada de carbono individual vai continuar entre as mais altas do planeta!!!",
        "texto_medio": "seu resultado é mediano nisso, tente compensar suas viagens com ações sustentáveis. Caso aumente a frequência, suas emissões de CO2 vão crescer bastante!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue evitando voos desnecessários. Caso comece a viajar de avião com frequência, sua pegada de carbono vai aumentar rapidamente!!!",
    },
    {
        "chave": "reciclagem", "icone": "♻️", "rotulo": "Reciclagem",
        "pergunta": "Quantos itens você recicla por semana?",
        "unidade": "item(ns) por semana",
        "peso": 1, "bonus": True, "min": 0, "max": 20, "padrao": 4,
        "limite_alto": 2, "limite_medio": 6,
        "texto_alto": "seu resultado é péssimo nisso, comece a separar seus materiais recicláveis agora mesmo. Caso não faça isso, o lixo vai continuar se acumulando e poluindo o planeta!!!",
        "texto_medio": "seu resultado é mediano nisso, tente reciclar mais itens do seu dia a dia. Caso não faça isso, muito material reaproveitável vai continuar sendo desperdiçado!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue reciclando bastante. Caso pare de reciclar, mais lixo vai parar em aterros e no meio ambiente!!!",
    },
    {
        "chave": "transporte_sustentavel", "icone": "🚲", "rotulo": "Transporte sustentável",
        "pergunta": "Quantos dias por semana você usa transporte público, bicicleta ou caminha para se locomover?",
        "unidade": "dia(s) por semana",
        "peso": 2, "bonus": True, "min": 0, "max": 7, "padrao": 2,
        "limite_alto": 1, "limite_medio": 3,
        "texto_alto": "seu resultado é péssimo nisso, tente usar mais transporte público, bicicleta ou caminhar. Caso não faça isso, sua dependência do carro individual vai continuar gerando mais poluição!!!",
        "texto_medio": "seu resultado é mediano nisso, continue aumentando o uso de transporte sustentável. Caso diminua, seu impacto no trânsito e na poluição vai voltar a crescer!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue priorizando transporte sustentável. Caso abandone esse hábito, sua pegada de carbono vai aumentar rapidamente!!!",
    },
    {
        "chave": "compostagem", "icone": "🌱", "rotulo": "Compostagem",
        "pergunta": "Quantos itens orgânicos (restos de comida, cascas, folhas) você composta por semana?",
        "unidade": "item(ns) por semana",
        "peso": 1, "bonus": True, "min": 0, "max": 20, "padrao": 1,
        "limite_alto": 1, "limite_medio": 5,
        "texto_alto": "seu resultado é péssimo nisso, comece a compostar restos de comida e folhas agora mesmo. Caso não faça isso, mais lixo orgânico vai continuar parando em aterros e gerando gases do efeito estufa!!!",
        "texto_medio": "seu resultado é mediano nisso, tente aumentar a quantidade de itens compostados. Caso não faça isso, você vai perder a chance de reduzir ainda mais seu lixo!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue compostando bastante. Caso pare de compostar, mais lixo orgânico vai voltar a poluir aterros sanitários!!!",
    },
    {
        "chave": "compras_online", "icone": "📦", "rotulo": "Compras online",
        "pergunta": "Quantas entregas de compras online (e-commerce) você recebe por semana?",
        "unidade": "entrega(s) por semana",
        "peso": 3, "bonus": False, "min": 0, "max": 10, "padrao": 2,
        "limite_alto": 5, "limite_medio": 2,
        "texto_alto": "seu resultado é péssimo nisso, tente juntar compras em um pedido só e evitar entregas urgentes. Caso não faça isso, o transporte extra e as embalagens descartáveis vão continuar se multiplicando!!!",
        "texto_medio": "seu resultado é mediano nisso, tente planejar melhor suas compras para reduzir o número de entregas. Caso não faça isso, o impacto do frete e das embalagens vai continuar crescendo!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue evitando compras por impulso. Caso comece a pedir entregas em excesso, o transporte e o lixo de embalagens vão disparar rapidamente!!!",
    },
    {
        "chave": "streaming", "icone": "📺", "rotulo": "Streaming e vídeos",
        "pergunta": "Quantas horas por dia você passa assistindo streaming ou vídeos online?",
        "unidade": "hora(s) por dia",
        "peso": 1, "bonus": False, "min": 0, "max": 12, "padrao": 3,
        "limite_alto": 6, "limite_medio": 3,
        "texto_alto": "seu resultado é péssimo nisso, tente reduzir o tempo de tela e preferir qualidade de vídeo menor quando possível. Caso não faça isso, o consumo de energia dos data centers vai continuar crescendo!!!",
        "texto_medio": "seu resultado é mediano nisso, tente diminuir um pouco o tempo diário de streaming. Caso não faça isso, seu consumo de dados e energia vai continuar alto!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue controlando o tempo de tela. Caso aumente muito, o consumo de energia por trás do streaming vai crescer rapidamente!!!",
    },
    {
        "chave": "papel", "icone": "🖨️", "rotulo": "Impressão de papel",
        "pergunta": "Quantas folhas de papel você imprime por semana?",
        "unidade": "folha(s) por semana",
        "peso": 1, "bonus": False, "min": 0, "max": 100, "padrao": 10,
        "limite_alto": 40, "limite_medio": 15,
        "texto_alto": "seu resultado é péssimo nisso, tente digitalizar documentos e imprimir só o essencial. Caso não faça isso, o desmatamento ligado à produção de papel vai continuar aumentando!!!",
        "texto_medio": "seu resultado é mediano nisso, tente reduzir aos poucos as impressões desnecessárias. Caso não faça isso, o consumo de papel e água na produção dele vai continuar alto!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue priorizando o digital. Caso volte a imprimir em excesso, o consumo de papel vai voltar a crescer rapidamente!!!",
    },
    {
        "chave": "eletronicos", "icone": "🔌", "rotulo": "Troca de eletrônicos",
        "pergunta": "Quantas vezes por ano você troca de celular ou eletrônicos ainda funcionando?",
        "unidade": "vez(es) por ano",
        "peso": 8, "bonus": False, "min": 0, "max": 5, "padrao": 0,
        "limite_alto": 2, "limite_medio": 1,
        "texto_alto": "seu resultado é péssimo nisso, tente usar seus aparelhos por mais tempo e consertar antes de trocar. Caso não faça isso, o lixo eletrônico e a mineração de metais raros vão continuar disparando!!!",
        "texto_medio": "seu resultado é mediano nisso, tente esperar mais tempo antes de trocar de aparelho. Caso não faça isso, o descarte de eletrônicos vai continuar crescendo!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue usando seus aparelhos até o fim da vida útil. Caso comece a trocar com frequência, o lixo eletrônico vai aumentar rapidamente!!!",
    },
    {
        "chave": "agua_torneira", "icone": "🚰", "rotulo": "Torneira aberta à toa",
        "pergunta": "Quantos minutos por dia você deixa a torneira aberta à toa (escovando dentes, lavando louça, etc)?",
        "unidade": "minuto(s) por dia",
        "peso": 1, "bonus": False, "min": 0, "max": 30, "padrao": 5,
        "limite_alto": 15, "limite_medio": 6,
        "texto_alto": "seu resultado é péssimo nisso, feche a torneira sempre que não estiver usando a água diretamente. Caso não faça isso, o desperdício de água tratada vai continuar crescendo!!!",
        "texto_medio": "seu resultado é mediano nisso, tente prestar mais atenção e fechar a torneira nos intervalos. Caso não faça isso, o consumo de água vai continuar acima do necessário!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue fechando a torneira sempre que possível. Caso relaxe esse hábito, o desperdício de água vai voltar a crescer!!!",
    },
    {
        "chave": "arvores", "icone": "🌳", "rotulo": "Plantio de árvores",
        "pergunta": "Quantas árvores ou plantas você cuida ou plantou nos últimos 12 meses?",
        "unidade": "árvore(s)/planta(s) por ano",
        "peso": 3, "bonus": True, "min": 0, "max": 10, "padrao": 1,
        "limite_alto": 0, "limite_medio": 3,
        "texto_alto": "seu resultado é péssimo nisso, tente plantar ou cuidar de pelo menos uma árvore ou planta este ano. Caso não faça isso, você perde uma forma simples de compensar suas próprias emissões!!!",
        "texto_medio": "seu resultado é mediano nisso, tente aumentar aos poucos o número de árvores ou plantas que você cuida. Caso não faça isso, você deixa de aproveitar um jeito fácil de ajudar o planeta!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue plantando e cuidando de árvores e plantas. Caso pare com esse hábito, você perde um efeito positivo real sobre o ambiente ao seu redor!!!",
    },
    {
        "chave": "produtos_locais", "icone": "🥕", "rotulo": "Alimentos locais/orgânicos",
        "pergunta": "Quantas refeições por semana você faz com alimentos locais, orgânicos ou de produtor direto?",
        "unidade": "refeição(ões) por semana",
        "peso": 1, "bonus": True, "min": 0, "max": 21, "padrao": 3,
        "limite_alto": 2, "limite_medio": 8,
        "texto_alto": "seu resultado é péssimo nisso, tente incluir mais alimentos locais ou orgânicos na sua rotina. Caso não faça isso, você continua dependendo mais de cadeias produtivas com maior impacto de transporte e agrotóxicos!!!",
        "texto_medio": "seu resultado é mediano nisso, tente aumentar aos poucos a proporção de alimentos locais ou orgânicos. Caso não faça isso, você deixa passar uma forma simples de reduzir seu impacto na alimentação!!!",
        "texto_baixo": "seu resultado é ótimo nisso, continue priorizando produtores locais e orgânicos. Caso volte a depender só de grandes cadeias produtivas, seu impacto ambiental na alimentação vai voltar a crescer!!!",
    },
]

FAIXA_BAIXO = 100
FAIXA_MEDIO = 210
PONTUACAO_MAXIMA_VISUAL = 380

COR_POR_NIVEL = {
    "baixo": "#3f9469",
    "medio": "#c97b3b",
    "alto": "#b4452f",
}

CATEGORIAS_POR_CHAVE = {c["chave"]: c for c in CATEGORIAS}


def valores_padrao() -> dict:
    return {c["chave"]: c["padrao"] for c in CATEGORIAS}


def calcular_pontuacao(valores: dict) -> int:
    total = 0
    for c in CATEGORIAS:
        valor = valores.get(c["chave"], 0)
        pontos_categoria = valor * c["peso"]
        total += -pontos_categoria if c["bonus"] else pontos_categoria
    return max(total, 0)


def nivel_categoria(categoria: dict, valor: int) -> str:
    if categoria["bonus"]:
        if valor <= categoria["limite_alto"]:
            return "alto"
        elif valor <= categoria["limite_medio"]:
            return "medio"
        return "baixo"
    else:
        if valor >= categoria["limite_alto"]:
            return "alto"
        elif valor >= categoria["limite_medio"]:
            return "medio"
        return "baixo"


def classificar(pontos: int):
    if pontos <= FAIXA_BAIXO:
        return ("baixo", "Impacto BAIXO", "✅", "Parabéns! Seus hábitos já ajudam bastante o planeta.")
    elif pontos <= FAIXA_MEDIO:
        return ("medio", "Impacto MÉDIO", "⚠️", "Você está no caminho certo, mas ainda dá para melhorar.")
    else:
        return ("alto", "Impacto ALTO", "❌", "Seus hábitos atuais pesam bastante sobre o meio ambiente.")


def calcular_percentual_gauge(pontos: int) -> int:
    percentual = int((pontos / PONTUACAO_MAXIMA_VISUAL) * 100)
    return max(0, min(percentual, 100))


def montar_barras_categoria(valores: dict):
    pontos_por_categoria = {
        c["chave"]: valores.get(c["chave"], 0) * c["peso"] for c in CATEGORIAS
    }

    maior = max(pontos_por_categoria.values(), default=1)
    if maior <= 0:
        maior = 1

    barras = []
    for c in CATEGORIAS:
        pts = pontos_por_categoria[c["chave"]]
        nivel = nivel_categoria(c, valores.get(c["chave"], 0))
        barras.append({
            "chave": c["chave"],
            "icone": c["icone"],
            "rotulo": c["rotulo"],
            "bonus": c["bonus"],
            "pts": pts,
            "pct": int((pts / maior) * 100),
            "cor": COR_POR_NIVEL[nivel],
        })
    return barras


def gerar_recomendacoes(valores: dict):
    recomendacoes = []
    for c in CATEGORIAS:
        valor = valores.get(c["chave"], 0)
        nivel = nivel_categoria(c, valor)
        texto = {"alto": c["texto_alto"], "medio": c["texto_medio"], "baixo": c["texto_baixo"]}[nivel]

        recomendacoes.append({
            "icone": c["icone"],
            "pergunta": c["pergunta"],
            "resposta": f"{valor} {c['unidade']}",
            "texto": texto,
            "nivel": nivel,
        })
    return recomendacoes


def valor_formulario_seguro(form, chave_categoria: str) -> int:
    categoria = CATEGORIAS_POR_CHAVE[chave_categoria]
    bruto = form.get(chave_categoria, categoria["padrao"])

    try:
        valor = int(float(bruto))
    except (TypeError, ValueError):
        valor = categoria["padrao"]

    return max(categoria["min"], min(valor, categoria["max"]))


@app.route("/", methods=["GET", "POST"])
def inicio():
    resultado = None
    recomendacoes = []
    valores = valores_padrao()

    if request.method == "POST":
        valores = {
            c["chave"]: valor_formulario_seguro(request.form, c["chave"])
            for c in CATEGORIAS
        }

        pontos = calcular_pontuacao(valores)
        nivel, titulo, emoji, mensagem = classificar(pontos)
        percentual_gauge = calcular_percentual_gauge(pontos)
        barras = montar_barras_categoria(valores)

        resultado = {
            "nivel": nivel,
            "titulo": titulo,
            "emoji": emoji,
            "mensagem": mensagem,
            "pontos": pontos,
            "percentual_gauge": percentual_gauge,
            "maximo_visual": PONTUACAO_MAXIMA_VISUAL,
            "cor_gauge": COR_POR_NIVEL[nivel],
            "barras": barras,
        }

        recomendacoes = gerar_recomendacoes(valores)

    categorias_para_js = [
        {"chave": c["chave"], "peso": c["peso"], "bonus": c["bonus"]}
        for c in CATEGORIAS
    ]

    return render_template(
        "index.html",
        resultado=resultado,
        recomendacoes=recomendacoes,
        valores=valores,
        categorias=CATEGORIAS,
        categorias_json=json.dumps(categorias_para_js),
        faixa_baixo=FAIXA_BAIXO,
        faixa_medio=FAIXA_MEDIO,
    )


if __name__ == "__main__":
    app.run(debug=True)