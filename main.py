import streamlit as st
from utils import extrair_texto_docx, extrair_texto_pdf
from openai_assistant import enviar_para_openai

st.set_page_config(layout="wide", page_title="Agente Jurídico Prefeitura Goiania", initial_sidebar_state="expanded")

with st.sidebar:
    st.image("logo_eug.png", width=220)
    st.markdown(
        """
        <div style='background-color:#111124;padding:20px;border-radius:10px; text-align:center; margin-top: 10px;'>
            <a href='#' style='color:#fff;text-decoration:none;'><b>Agente</b></a>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.title("Análise Jurídica do Termo de Referência")

if "historico" not in st.session_state:
    st.session_state["historico"] = []

# CAMPOS DO FORMULÁRIO PRINCIPAL
with st.form(key="form_envio", clear_on_submit=False):
    uploaded_file = st.file_uploader("Anexe um arquivo Word (.docx) ou PDF (.pdf):", type=["docx", "pdf"])
    prompt_extra = st.text_area("Observações adicionais (opcional):", height=100, key="prompt")
    col1, col2 = st.columns([1, 1])
    enviar = col1.form_submit_button("Enviar para análise")
    limpar = col2.form_submit_button("Limpar histórico")

if limpar:
    st.session_state["historico"] = []
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

for idx, item in enumerate(reversed(st.session_state["historico"])):
    st.markdown(f"**Arquivo analisado:** {item['documento']}")
    if item['prompt']:
        st.markdown(f"**Observações:** {item['prompt']}")
    st.markdown("---")
    st.markdown(item["resposta"], unsafe_allow_html=True)
    st.markdown("---")

# Fecha a div do frame principal
st.markdown("</div>", unsafe_allow_html=True)
