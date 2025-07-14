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

st.title("Análise Jurídica  - Licitações")

if "historico" not in st.session_state:
    st.session_state["historico"] = []

if "texto_edital" not in st.session_state:
    st.session_state["texto_edital"] = None

# ---- QUEBRA-GELO (BOTÕES) ----
st.subheader("Modelos rápidos")
colq1, colq2, colq3 = st.columns(3)

if colq1.button("Gerar edital de licitação"):
    st.session_state["texto_edital"] = """
**EDITAL DE LICITAÇÃO Nº ___/2025 – PREGÃO ELETRÔNICO**

A PREFEITURA MUNICIPAL DE [NOME], por meio do(a) [Secretaria/Departamento], torna público para conhecimento dos interessados que realizará licitação na modalidade Pregão Eletrônico, do tipo menor preço, nos termos da Lei nº 14.133/2021, para contratação de [OBJETO].

1. **DO OBJETO**  
Contratação de empresa especializada em [descrever objeto], conforme especificações constantes no Termo de Referência – Anexo I deste Edital.

2. **DA ABERTURA**  
- Data: [DATA]  
- Horário: [HORÁRIO]  
- Plataforma: www.gov.br/compras

3. **DAS CONDIÇÕES DE PARTICIPAÇÃO**  
[Requisitos básicos, vedações, ME/EPP, consórcios, etc.]

4. **DO CRITÉRIO DE JULGAMENTO**  
Menor preço global / por item (especificar)

5. **DOS DOCUMENTOS DE HABILITAÇÃO**  
[Documentos jurídicos, fiscais, qualificação técnica, etc.]

6. **DAS CONDIÇÕES DE PAGAMENTO**  
[Forma, prazos, reajuste, retenções]

7. **DAS SANÇÕES ADMINISTRATIVAS**  
[Advertência, multa, suspensão, etc.]

8. **DAS DISPOSIÇÕES FINAIS**  
[Esclarecimentos, impugnações, foro competente]

[Município], [Data]

[Nome do(a) Gestor(a)]  
[Cargo]
    """

if colq2.button("Criar termo de referência"):
    prompt_quebragelo = "mostrar conteudo do arquivo: template_termo_referencia.txt que esta na minha base de conhecimento."
    with st.spinner("Criando termo de referência..."):
        resposta = enviar_para_openai(prompt_quebragelo, usar_prompt_padrao=False)
    st.session_state["historico"].append({
        "documento": "Quebra-gelo: Termo de Referência",
        "prompt": prompt_quebragelo,
        "resposta": resposta,
    })
    st.session_state["texto_edital"] = None

if colq3.button("Redigir minuta de contrato"):
    prompt_quebragelo = "mostrar conteudo do arquivo: template_minuta_contrato.txt que esta na minha base de conhecimento."
    with st.spinner("Redigindo minuta de contrato..."):
        resposta = enviar_para_openai(prompt_quebragelo, usar_prompt_padrao=False)
    st.session_state["historico"].append({
        "documento": "Quebra-gelo: Minuta de Contrato",
        "prompt": prompt_quebragelo,
        "resposta": resposta,
    })
    st.session_state["texto_edital"] = None

# ---- MOSTRAR TEXTO DO EDITAL DE LICITAÇÃO SE CLICADO ----
if st.session_state["texto_edital"]:
    st.markdown("---")
    st.markdown("### Modelo: Edital de Licitação")
    st.markdown(st.session_state["texto_edital"])
    st.markdown("---")

# ---- FORMULÁRIO NORMAL ----
with st.form(key="form_envio", clear_on_submit=False):
    uploaded_file = st.file_uploader("Anexe um arquivo Word (.docx) ou PDF (.pdf):", type=["docx", "pdf"])
    prompt_extra = st.text_area("Observações adicionais (opcional):", height=100, key="prompt")
    col1, col2 = st.columns([1, 1])
    enviar = col1.form_submit_button("Enviar para análise")
    limpar = col2.form_submit_button("Limpar histórico")

if limpar:
    st.session_state["historico"] = []
    st.session_state["texto_edital"] = None
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
        st.session_state["texto_edital"] = None

# ---- EXIBIR HISTÓRICO ----
for idx, item in enumerate(reversed(st.session_state["historico"])):
    st.markdown(f"**Arquivo analisado:** {item['documento']}")
    if item['prompt']:
        st.markdown(f"**Prompt enviado:** `{item['prompt']}`")
    st.markdown("---")
    st.markdown(item["resposta"], unsafe_allow_html=True)
    st.markdown("---")
