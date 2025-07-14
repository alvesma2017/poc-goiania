import docx
import PyPDF2

def extrair_texto_docx(file):
    doc = docx.Document(file)
    texto = "\n".join([p.text for p in doc.paragraphs])
    return texto

def extrair_texto_pdf(file):
    reader = PyPDF2.PdfReader(file)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() + "\n"
    return texto
