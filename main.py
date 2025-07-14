import streamlit as st
from utils import extrair_texto_docx, extrair_texto_pdf
from openai_assistant import enviar_para_openai

st.set_page_config(layout="wide", page_title="Agente Jurídico Prefeitura Goiania", initial_sidebar_state="expanded")

with st.sidebar:
    st.image("logo_eug.png", width=220)
    st.markdown(
        """
        <div style='background-color:#111124;padding:20px;border-radius:10px; text-align:center; margin-top: 10px;'>
            <a href='#' style='color:#fff;text-decoration:none;'><b></b></a>
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

# ---- FORMULÁRIO NORMAL ----
with st.form(key="form_envio", clear_on_submit=False):
    uploaded_file = st.file_uploader("Anexe um arquivo Word (.docx) ou PDF (.pdf):", type=["docx", "pdf"])
    prompt_extra = st.text_area("Observações, texto ou conteúdo para análise (opcional):", height=100, key="prompt")
    col1, col2 = st.columns([1, 1])
    enviar = col1.form_submit_button("Analisar (arquivo e/ou texto)")
    limpar = col2.form_submit_button("Limpar histórico")

if limpar:
    st.session_state["historico"] = []
    st.session_state["texto_modelo"] = None
    st.session_state["titulo_modelo"] = None
    st.experimental_rerun()

if enviar:
    texto = ""
    nome_doc = ""
    # Se tiver arquivo, prioriza arquivo
    if uploaded_file is not None:
        nome_doc = uploaded_file.name
        if uploaded_file.type == "application/pdf":
            texto = extrair_texto_pdf(uploaded_file)
        else:
            texto = extrair_texto_docx(uploaded_file)
        # prompt_extra pode ser complementar (campo de texto é opcional)
        resposta = enviar_para_openai(texto, prompt_extra)
        st.session_state["historico"].append({
            "documento": nome_doc,
            "prompt": prompt_extra,
            "resposta": resposta,
        })
        st.session_state["texto_modelo"] = None
        st.session_state["titulo_modelo"] = None
    elif prompt_extra.strip():
        # Se não tem arquivo, mas tem texto no campo textarea
        resposta = enviar_para_openai(prompt_extra, "", usar_prompt_padrao=True)
        st.session_state["historico"].append({
            "documento": "Texto digitado",
            "prompt": prompt_extra,
            "resposta": resposta,
        })
        st.session_state["texto_modelo"] = None
        st.session_state["titulo_modelo"] = None
    else:
        st.error("Por favor, anexe um arquivo ou digite um texto para análise.")

# ---- QUEBRA-GELO (BOTÕES) ABAIXO DO FORMULÁRIO ----
st.markdown("---")
st.subheader("Modelos rápidos")
colq1, colq2, colq3 = st.columns(3)

if colq1.button("Gerar edital de licitação"):
    st.session_state["titulo_modelo"] = "Modelo: Edital de Licitação"
    st.session_state["texto_modelo"] = """
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
    st.session_state["titulo_modelo"] = "Modelo: Termo de Referência"
    st.session_state["texto_modelo"] = """
**TERMO DE REFERÊNCIA**

1. **OBJETO**  
Contratação de empresa especializada em [descrever], conforme condições, quantidades e exigências estabelecidas neste Termo de Referência.

2. **JUSTIFICATIVA DA CONTRATAÇÃO**  
[Fundamentar com base no interesse público, eficiência administrativa ou necessidade técnica. Ex: Art. 18, I e §1º da Lei 14.133/21]

3. **ESPECIFICAÇÃO DO OBJETO**  
[Descrição técnica detalhada, unidades, prazo de entrega, garantias, local da execução]

4. **PRAZO DE EXECUÇÃO E VIGÊNCIA CONTRATUAL**  
Prazo estimado: [___] meses

5. **REQUISITOS DE HABILITAÇÃO**  
[Certidões, experiência mínima, qualificação técnica, alvarás]

6. **FISCALIZAÇÃO E GESTÃO DO CONTRATO**  
[Nome do fiscal do contrato ou órgão responsável]

7. **CRITÉRIOS DE PAGAMENTO**  
[Medição, periodicidade, documentos exigidos, glosa]

8. **ORÇAMENTO ESTIMADO**  
Valor estimado: R$ [__] (conforme cotação de mercado / pesquisa PNCP / SINAPI / etc.)

Elaborado por:  
[Responsável técnico], [cargo]  
[Data]
    """

if colq3.button("Redigir minuta de contrato"):
    st.session_state["titulo_modelo"] = "Modelo: Minuta de Contrato"
    st.session_state["texto_modelo"] = """
**MINUTA DE CONTRATO ADMINISTRATIVO Nº ___/2025**

CONTRATANTE: Município de [NOME], com sede à [endereço], inscrito no CNPJ sob o nº [___].  
CONTRATADA: [RAZÃO SOCIAL], CNPJ nº [___], com sede à [endereço].

As partes acima identificadas resolvem celebrar o presente Contrato Administrativo, com fundamento no processo licitatório nº ___/2025, modalidade [MODALIDADE], nos termos da Lei nº 14.133/2021, mediante as cláusulas e condições a seguir:

**CLÁUSULA PRIMEIRA – DO OBJETO**  
[Descrever detalhadamente o objeto do contrato]

**CLÁUSULA SEGUNDA – DO PRAZO**  
[Determinar o prazo de vigência e execução]

**CLÁUSULA TERCEIRA – DO VALOR E PAGAMENTO**  
[Valor global ou por item, condições de pagamento, reajuste]

**CLÁUSULA QUARTA – DAS OBRIGAÇÕES DA CONTRATANTE**  
[Listar obrigações, como fiscalizar, pagar, etc.]

**CLÁUSULA QUINTA – DAS OBRIGAÇÕES DA CONTRATADA**  
[Listar entregas, prazos, normas técnicas, sigilo]

**CLÁUSULA SEXTA – DAS PENALIDADES**  
[Advertência, multa, suspensão – conforme art. 156 da Lei 14.133/2021]

**CLÁUSULA SÉTIMA – DA RESCISÃO**  
[Hipóteses previstas em lei]

**CLÁUSULA OITAVA – DO FORO**  
[Indicar foro da comarca do Município]

E por estarem justas e contratadas, firmam o presente contrato em [nº] vias de igual teor e forma.

[Município], [Data]

__________________________  
PREFEITURA MUNICIPAL

__________________________  
CONTRATADA
    """

# ---- MOSTRAR TEXTO DO MODELO ESCOLHIDO (SE ALGUM FOI CLICADO) ----
if st.session_state["texto_modelo"]:
    st.markdown("---")
    st.markdown(f"### {st.session_state['titulo_modelo']}")
    st.markdown(st.session_state["texto_modelo"])
    st.markdown("---")

# ---- EXIBIR HISTÓRICO ----
for idx, item in enumerate(reversed(st.session_state["historico"])):
    st.markdown(f"**Arquivo analisado:** {item['documento']}")
    if item['prompt']:
        st.markdown(f"**Prompt enviado:** `{item['prompt']}`")
    st.markdown("---")
    st.markdown(item["resposta"], unsafe_allow_html=True)
    st.markdown("---")
