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

# ---- QUEBRA-GELO (BOTÕES) ----
st.subheader("Modelos rápidos")

colq1, colq2, colq3 = st.columns(3)

if colq1.button("Gerar edital de licitação"):
    prompt_quebragelo = "mostrar conteudo do arquivo: template_edital_pregao.txt que esta na minha base de conhecimento."
    with st.spinner("Gerando edital de licitação..."):
        resposta = enviar_para_openai(prompt_quebragelo, usar_prompt_padrao=False)
    st.session_state["historico"].append({
        "documento": "Quebra-gelo: Edital de Licitação",
        "prompt": prompt_quebragelo,
        "resposta": resposta,
    })

if colq2.button("Criar termo de referência"):
    prompt_quebragelo = "mostrar conteudo do arquivo: template_termo_referencia.txt que esta na minha base de conhecimento."
    with st.spinner("Criando termo de referência..."):
        resposta = enviar_para_openai(prompt_quebragelo, usar_prompt_padrao=False)
    st.session_state["historico"].append({
        "documento": "Quebra-gelo: Termo de Referência",
        "prompt": prompt_quebragelo,
        "resposta": resposta,
    })

if colq3.button("Redigir minuta de contrato"):
    prompt_quebragelo = "mostrar conteudo do arquivo: template_minuta_contrato.txt que esta na minha base de conhecimento."
    with st.spinner("Redigindo minuta de contrato..."):
        resposta = enviar_para_openai(prompt_quebragelo, usar_prompt_padrao=False)
    st.session_state["historico"].append({
        "documento": "Quebra-gelo: Minuta de Contrato",
        "prompt": prompt_quebragelo,
        "resposta": resposta,
    })

# ---- FORMULÁRIO NORMAL ----
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
            resposta = enviar_para_openai(texto, prompt_extra)  # usar_prompt_padrao=True (padrão)
            st.session_state["historico"].append({
                "documento": uploaded_file.name,
                "prompt": prompt_extra,
                "resposta": resposta,
            })

# ---- EXIBIR HISTÓRICO ----
for idx, item in enumerate(reversed(st.session_state["historico"])):
    st.markdown(f"**Arquivo analisado:** {item['documento']}")
    if item['prompt']:
        st.markdown(f"**Prompt enviado:** `{item['prompt']}`")
    st.markdown("---")
    st.markdown(item["resposta"], unsafe_allow_html=True)
    st.markdown("---")
