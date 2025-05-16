import streamlit as st
import pdfplumber
import difflib
import io
from docx import Document

st.set_page_config(page_title="Word/PDF Karşılaştırıcı", layout="wide")
st.title("📄 Word / PDF Dosya Karşılaştırıcı")

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def show_diff(text1, text2):
    d = difflib.HtmlDiff()
    result = d.make_table(
        text1.splitlines(), text2.splitlines(),
        context=True, numlines=2
    )
    return result

file1 = st.file_uploader("🔹 1. Dosyayı Yükleyin (PDF/DOCX)", type=["pdf", "docx"], key="file1")
file2 = st.file_uploader("🔸 2. Dosyayı Yükleyin (PDF/DOCX)", type=["pdf", "docx"], key="file2")

if file1 and file2:
    if file1.type == "application/pdf":
        text1 = extract_text_from_pdf(file1)
    else:
        text1 = extract_text_from_docx(file1)

    if file2.type == "application/pdf":
        text2 = extract_text_from_pdf(file2)
    else:
        text2 = extract_text_from_docx(file2)

    st.markdown("### 🧠 Metin Farkları")
    diff_html = show_diff(text1, text2)
    st.components.v1.html(diff_html, height=500, scrolling=True)
