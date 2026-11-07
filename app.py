import json
from urllib.parse import quote
 
import streamlit as st
 
NOME_LOJA = "Lanchonete"
# Número com código do país e DDD, ex.: "5511999999999".
# Deixe vazio para esconder o botão de enviar pelo WhatsApp.
WHATSAPP = ""
 
st.set_page_config(page_icon="🍔", page_title=NOME_LOJA)
 
cardapio = {
    "🥟 Salgados": {
        "Coxinha": 6,
        "Risole": 7,
        "Pastel de carne": 8,
        "Pastel de queijo": 8,
        "Esfiha de carne": 6.5,
        "Empada de frango": 6,
        "Pão de queijo": 4,
        "Enroladinho de salsicha": 5.5,
    },
    "🍔 Lanches": {
        "X-Burguer": 16,
        "X-Salada": 18,
        "X-Bacon": 22,
        "Hot dog": 12,
        "Misto quente": 9,
        "Pão na chapa": 5,
    },
    "🍟 Porções": {
        "Batata frita": 18,
    },
    "🥤 Bebidas": {
        "Coca lata 350 ml": 3.5,
        "Guaraná lata 350 ml": 3.5,
        "Suco natural": 8,
        "Água mineral": 3,
        "Café": 4,
    },
    "🍮 Doces": {
        "Brigadeiro": 3,
        "Pudim": 7,
    },
}
 
PRECOS = {item: preco for itens in cardapio.values() for item, preco in itens.items()}
 
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Figtree:wght@400;500;700&display=swap');
 
.stApp { background: #F4F7F5; color: #13261C; font-family: 'Figtree', sans-serif; }
.stApp button, .stApp [role="tab"] { font-family: 'Figtree', sans-serif; }
.block-container { max-width: 640px; padding: 2rem 1rem 7rem; }
footer, #MainMenu { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
 
/* Topo */
.topo { background: #FFC21A; border-radius: 20px; padding: 1.6rem 1.4rem 1.4rem; margin-bottom: 1.2rem; }
.topo .nome { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 3rem;
              line-height: 1; letter-spacing: -0.02em; margin: 0; }
.topo .sub { margin: .6rem 0 0; font-size: 1.05rem; }
 
/* Abas de categoria */
.stTabs [data-baseweb="tab"] { font-weight: 700; font-size: 1rem; }
 
/* Linha de item: nome/preço à esquerda, − qtd + à direita (também no celular) */
[class*="st-key-linha_"] { border-bottom: 1px dashed #B9C6BE; padding: .4rem 0; }
[class*="st-key-linha_"] [data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important; gap: .4rem !important; align-items: center;
}
[class*="st-key-linha_"] [data-testid="stColumn"] { min-width: 0 !important; }
[class*="st-key-linha_"] [data-testid="stColumn"]:first-child { flex: 1 1 0 !important; width: auto !important; }
[class*="st-key-linha_"] [data-testid="stColumn"]:not(:first-child) { flex: 0 0 2.5rem !important; width: 2.5rem !important; }
 
[class*="st-key-linha_"] .stButton > button {
    width: 2.5rem; height: 2.5rem; min-height: 0; padding: 0; border-radius: 50%;
    border: 2px solid #13261C; background: #fff; color: #13261C; line-height: 1;
}
[class*="st-key-linha_"] .stButton > button p { font-size: 1.3rem; font-weight: 700; }
[class*="st-key-linha_"] .stButton > button:hover:not(:disabled) { background: #FFC21A; color: #13261C; border-color: #13261C; }
[class*="st-key-linha_"] .stButton > button:disabled { opacity: .35; }
 
.item-nome { font-weight: 700; font-size: 1.05rem; line-height: 1.25; }
.item-preco { color: #4A6355; font-size: .95rem; }
.qtd { text-align: center; font-weight: 700; font-size: 1.15rem; color: #5F7266; }
.qtd.on { color: #D62828; }
 
/* Resumo do pedido, no formato de comanda */
.comanda { background: #fff; border: 1px solid #D5DED8; border-radius: 16px; padding: 1.2rem 1.2rem .5rem; margin: 1.5rem 0 1rem; }
.comanda .titulo { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 1.6rem; margin: 0 0 .4rem; }
.comanda-linha { display: flex; justify-content: space-between; gap: 1rem; padding: .55rem 0; border-bottom: 1px dashed #B9C6BE; }
.comanda-total { display: flex; justify-content: space-between; padding: .9rem 0 .7rem;
                 font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 1.6rem; }
.vazio { color: #4A6355; padding: .4rem 0 1rem; }
 
/* Botão principal */
button[data-testid="stBaseButton-primary"], a[data-testid="stBaseLinkButton-primary"] {
    background: #D62828; border-color: #D62828; color: #fff;
}
 
/* Barra fixa com o total */
.barra {
    position: fixed; left: 50%; transform: translateX(-50%); bottom: 1rem; z-index: 999;
    width: calc(100% - 2rem); max-width: 608px;
    display: flex; justify-content: space-between; align-items: center; gap: 1rem;
    background: #13261C; color: #fff !important; text-decoration: none !important;
    padding: .9rem 1.2rem; border-radius: 16px; box-shadow: 0 6px 20px rgba(0, 0, 0, .25);
}
.barra strong { font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.3rem; }
.barra .ver { color: #FFC21A; font-weight: 700; }
</style>
"""
 
 
def brl(valor):
    return f"R$ {valor:.2f}".replace(".", ",")
 
 
def carregar_pedido_da_url():
    """Lê o pedido salvo na URL (sobrevive ao recarregar a página)."""
    try:
        dados = json.loads(st.query_params.get("pedido", "{}"))
    except (json.JSONDecodeError, TypeError):
        return {}
    if not isinstance(dados, dict):
        return {}
    # Só aceita itens que existem no cardápio e quantidades válidas
    return {
        item: qtd
        for item, qtd in dados.items()
        if item in PRECOS and isinstance(qtd, int) and qtd > 0
    }
 
 
def salvar_pedido_na_url():
    """Grava o pedido atual na URL."""
    if st.session_state.pedido:
        st.query_params["pedido"] = json.dumps(
            st.session_state.pedido, ensure_ascii=False
        )
    elif "pedido" in st.query_params:
        del st.query_params["pedido"]
 
 
def alterar(item, delta):
    nova = st.session_state.pedido.get(item, 0) + delta
    if nova > 0:
        st.session_state.pedido[item] = nova
    else:
        st.session_state.pedido.pop(item, None)
    salvar_pedido_na_url()
 
 
def limpar():
    st.session_state.pedido = {}
    salvar_pedido_na_url()
 
 
# Ao abrir ou recarregar a página, recupera o pedido da URL
if "pedido" not in st.session_state:
    st.session_state.pedido = carregar_pedido_da_url()
 
st.markdown(CSS, unsafe_allow_html=True)
 
st.markdown(
    f'<div class="topo"><p class="nome">{NOME_LOJA}</p>'
    '<p class="sub">Toque em + para montar seu pedido.</p></div>',
    unsafe_allow_html=True,
)
 
# --- Cardápio por categoria ---
abas = st.tabs(list(cardapio.keys()))
 
for c, (aba, itens) in enumerate(zip(abas, cardapio.values())):
    with aba:
        for i, (item, preco) in enumerate(itens.items()):
            qtd = st.session_state.pedido.get(item, 0)
            with st.container(key=f"linha_{c}_{i}"):
                col_nome, col_menos, col_qtd, col_mais = st.columns(
                    [5, 1, 1, 1], vertical_alignment="center"
                )
                col_nome.markdown(
                    f'<div class="item-nome">{item}</div>'
                    f'<div class="item-preco">{brl(preco)}</div>',
                    unsafe_allow_html=True,
                )
                col_menos.button(
                    "−", key=f"menos_{c}_{i}", on_click=alterar,
                    args=(item, -1), disabled=qtd == 0,
                    help=f"Tirar {item}",
                )
                col_qtd.markdown(
                    f'<div class="qtd{" on" if qtd else ""}">{qtd}</div>',
                    unsafe_allow_html=True,
                )
                col_mais.button(
                    "+", key=f"mais_{c}_{i}", on_click=alterar,
                    args=(item, 1), help=f"Adicionar {item}",
                )
 
# --- Resumo do pedido ---
pedido = st.session_state.pedido
total = sum(PRECOS[item] * qtd for item, qtd in pedido.items())
n_itens = sum(pedido.values())
 
linhas = "".join(
    f'<div class="comanda-linha"><span>{qtd}× {item}</span>'
    f"<span>{brl(PRECOS[item] * qtd)}</span></div>"
    for item, qtd in pedido.items()
)
if pedido:
    corpo = (
        linhas
        + f'<div class="comanda-total"><span>Total</span><span>{brl(total)}</span></div>'
    )
else:
    corpo = (
        '<div class="vazio">Seu pedido está vazio. '
        "Escolha um item no cardápio para começar.</div>"
    )
 
st.markdown(
    f'<div id="seu-pedido"></div><div class="comanda">'
    f'<p class="titulo">Seu pedido</p>{corpo}</div>',
    unsafe_allow_html=True,
)
 
if pedido:
    col_limpar, col_whats = st.columns(2) if WHATSAPP else (st.container(), None)
    col_limpar.button("Limpar pedido", on_click=limpar, use_container_width=True)
 
    if WHATSAPP:
        texto = "Olá! Quero fazer um pedido:\n"
        texto += "\n".join(f"{qtd}x {item}" for item, qtd in pedido.items())
        texto += f"\nTotal: {brl(total)}"
        col_whats.link_button(
            "Enviar pelo WhatsApp",
            f"https://wa.me/{WHATSAPP}?text={quote(texto)}",
            type="primary",
            use_container_width=True,
        )
 
    # Barra fixa com o total, sempre visível enquanto o cliente rola o cardápio
    st.markdown(
        f'<a class="barra" href="#seu-pedido">'
        f'<span>{n_itens} {"item" if n_itens == 1 else "itens"}</span>'
        f"<strong>{brl(total)}</strong>"
        f'<span class="ver">Ver pedido</span></a>',
        unsafe_allow_html=True,
    )