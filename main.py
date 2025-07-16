import streamlit as st
from utils import extrair_texto_docx, extrair_texto_pdf
from openai_assistant import enviar_para_openai

st.set_page_config(layout="wide", page_title="Agente Jurídico Prefeitura Goiania", initial_sidebar_state="expanded")

with st.sidebar:
    st.image("logo_goi.png", width=220)
    st.markdown(
        """
        <div style='background-color:#111124;padding:20px;border-radius:10px; text-align:center; margin-top: 10px;'>
            <a href='/' style='color:#fff;text-decoration:none;'><b>Análise Jurídica</b></a>
        </div>
        <div style='background-color:#111124;padding:20px;border-radius:10px; text-align:center; margin-top: 20px;'>
            <a href='https://poc-goiania-gpt-v1.streamlit.app/' style='color:#fff;text-decoration:none;'><b>Gerar Documentação</b></a>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.title("Análise Jurídica - Licitações")

if "historico" not in st.session_state:
    st.session_state["historico"] = []

if "texto_modelo" not in st.session_state:
    st.session_state["texto_modelo"] = None
if "titulo_modelo" not in st.session_state:
    st.session_state["titulo_modelo"] = None

# ---- CSS para a textarea ----
st.markdown(
    """
    <style>
    textarea, .stTextArea textarea {
        border: 2px solid #111124 !important;
        border-radius: 8px !important;
        padding: 8px !important;
        box-shadow: none !important;
        outline: none !important;
        background: #F7F5F2 !important;
        font-size: 16px !important;
        color: #222 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- FORMULÁRIO NORMAL ----
with st.form(key="form_envio", clear_on_submit=False):
    uploaded_file = st.file_uploader("Anexe um arquivo Word (.docx) ou PDF (.pdf):", type=["docx", "pdf"])
    prompt_extra = st.text_area("Observações adicionais (opcional):", height=100, key="prompt")
    col1, col2 = st.columns([1, 1])
    enviar = col1.form_submit_button("Analise o arquivo - Termo de Referência, Edital de Licitação ou Minuta de Contratação (Anexar Arquivo)")
    limpar = col2.form_submit_button("Limpar histórico")

if limpar:
    st.session_state["historico"] = []
    st.session_state["texto_modelo"] = None
    st.session_state["titulo_modelo"] = None
    st.experimental_rerun()

if enviar:
    if uploaded_file is None:
        st.error("Por favor, anexe um arquivo Word ou PDF para análise.")
    else:
        with st.spinner("Analisando o documento..."):
            if uploaded_file.type == "application/pdf":
                texto = extrair_texto_pdf(uploaded_file)
            else:
                texto = extrair_texto_docx(uploaded_file)
            resposta = enviar_para_openai(texto, prompt_extra)
            st.session_state["historico"].append({
                "documento": uploaded_file.name,
                "prompt": prompt_extra,
                "resposta": resposta,
            })
        st.session_state["texto_modelo"] = None
        st.session_state["titulo_modelo"] = None

# ---- EXIBIR HISTÓRICO ----
for idx, item in enumerate(reversed(st.session_state["historico"])):
    st.markdown(f"**Arquivo analisado:** {item['documento']}")
    if item['prompt']:
        st.markdown(f"**Prompt enviado:** {item['prompt']}")
    st.markdown("---")
    st.markdown(item["resposta"], unsafe_allow_html=True)
    st.markdown("---")
