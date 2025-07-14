import openai
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = "asst_ke0QLnvj8WvqCvrr2YGB9uHV"

def enviar_para_openai(documento_texto, prompt_extra="", usar_prompt_padrao=True):
    """
    Se usar_prompt_padrao=True, concatena prompt base e análise de arquivo.
    Se usar_prompt_padrao=False, envia só o prompt_extra (ex: quebra-gelo).
    """
    openai.api_key = OPENAI_API_KEY

    if usar_prompt_padrao:
        prompt_base = """
Analise o documento em anexo, confirmando que se trata de um dos templates da base de conhecimento (Termo de Referência, Edital de Licitação ou Minuta de Contrato), caso não seja possível identificar o tipo do documento, solicite a informação ao usuário. Caso o documento anexado não seja um Termo de Referência, Edital de Licitação ou Minuta Contratual, informe que não será possível realizar a análise.

Após a confirmação de que o documento submetido é um Termo de Referência, Edital de Licitação ou Minuta de Contrato apresente, em tabela, as sugestões de adequação caso seja aplicável.

Na tabela, inclua:
O item ou trecho analisado,
O conteúdo atual,
A sugestão de texto/conteúdo revisado (ou seja, o novo texto exato que deve constar no documento),
A explicação do motivo para o ajuste, sempre fundamentada pela Lei 14.133/2021.
Exemplo de colunas:
Item analisado
Conteúdo atual
Sugestão de texto/conteúdo revisado
Fundamentação/justificativa (com base na Lei 14.133/2021)
Após a tabela, gere os textos revisados completos e formatados, prontos para serem inseridos diretamente no documento.
As sugestões devem ser objetivas, diretas e indicar o texto substitutivo, garantindo que o documento esteja plenamente adequado às exigências legais e melhores práticas da Administração Pública
"""
        full_prompt = prompt_base + "\n\nDocumento enviado:\n" + documento_texto
        if prompt_extra:
            full_prompt += "\n\nObservações adicionais do usuário:\n" + prompt_extra
    else:
        # Só manda o texto do prompt_extra (quebra-gelo)
        full_prompt = documento_texto.strip()  # Aqui deve vir o texto do botão quebra-gelo

    response = openai.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Você é um assistente jurídico especializado na Lei 14.133/2021."},
            {"role": "user", "content": full_prompt},
        ],
        temperature=0.1,
        max_tokens=10000
    )
    return response.choices[0].message.content
