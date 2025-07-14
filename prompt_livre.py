import streamlit as st
from openai_promptlivre import enviar_prompt_livre

st.set_page_config(layout="wide", page_title="Prompt Livre - Agente Jurídico", initial_sidebar_state="expanded")

st.title("Prompt Livre")

st.markdown("Use o campo abaixo para digitar um prompt livre ou clique no quebra-gelo:")

# Campo para prompt livre
prompt_text = st.text_area("Digite seu prompt", height=120)

col1, col2 = st.columns([2,1])
enviar = col1.button("Enviar para análise")
quebragelo = col2.button("Gerar Termo de referência (quebra-gelo)")

resposta = None

if enviar and prompt_text.strip():
    with st.spinner("Consultando OpenAI..."):
        resposta = enviar_prompt_livre(prompt_text.strip())
elif quebragelo:
    prompt_padrao = (
        "Gerar termo de referencia para aquisição de equipamentos de informática pela Prefeitura de Goiânia, "
        "com prazo de 12 meses, valor global de R$ 300.000,00, pagamento em até 30 dias, garantias legais, "
        "aplicação das penalidades previstas na Lei nº 14.133/2021, e fiscalização pelo Departamento de TI."
    )
    with st.spinner("Consultando OpenAI..."):
        resposta = enviar_prompt_livre(prompt_padrao)

if resposta:
    st.markdown("---")
    st.markdown("#### Resposta:")
    st.markdown(resposta, unsafe_allow_html=True)
