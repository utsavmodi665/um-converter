import os
import subprocess
from pathlib import Path
from docx2pdf import convert
from pdf2docx import Converter
from PIL import Image
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF
import shutil

# 🔥 Auto-detect LibreOffice
SOFFICE_PATH = shutil.which("soffice") or r"C:\Program Files\LibreOffice\program\soffice.exe"

# ---------------- DOCX → PDF ----------------
def docx_to_pdf(input_path, output_path):
    convert(input_path, output_path)
    return output_path

# ---------------- PDF → DOCX ----------------
def pdf_to_docx(input_path, output_path):
    cv = Converter(input_path)
    cv.convert(output_path)
    cv.close()
    return output_path

# ---------------- IMAGE → PDF ----------------
def image_to_pdf(input_path, output_path):
    img = Image.open(input_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(output_path)
    return output_path

# ---------------- PDF → IMAGE ----------------
def pdf_to_image(input_path, output_path):
    doc = fitz.open(input_path)
    paths = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap()
        out = output_path.replace(".png", f"_{i}.png")
        pix.save(out)
        paths.append(out)
    doc.close()
    return paths

# ---------------- TXT → PDF ----------------
def txt_to_pdf(input_path, output_path):
    c = canvas.Canvas(output_path)
    y = 800
    with open(input_path, encoding="utf-8") as f:
        for line in f:
            c.drawString(40, y, line.strip())
            y -= 20
            if y < 50:
                c.showPage()
                y = 800
    c.save()
    return output_path

# ---------------- PDF → TXT ----------------
def pdf_to_txt(input_path, output_path):
    reader = PdfReader(input_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    return output_path

# ---------------- PPTX ↔ PDF (FIXED) ----------------
def pptx_to_pdf(input_path, output_path):
    if not os.path.exists(SOFFICE_PATH):
        raise Exception("LibreOffice not found. Install LibreOffice or fix path.")

    subprocess.run([
        SOFFICE_PATH,
        "--headless",
        "--convert-to", "pdf",
        input_path,
        "--outdir", os.path.dirname(output_path)
    ], check=True)

    generated = input_path.rsplit(".", 1)[0] + ".pdf"
    if os.path.exists(generated):
        os.rename(generated, output_path)

    return output_path

def pdf_to_pptx(input_path, output_path):
    if not os.path.exists(SOFFICE_PATH):
        raise Exception("LibreOffice not found. Install LibreOffice or fix path.")

    subprocess.run([
        SOFFICE_PATH,
        "--headless",
        "--convert-to", "pptx",
        input_path,
        "--outdir", os.path.dirname(output_path)
    ], check=True)

    generated = input_path.rsplit(".", 1)[0] + ".pptx"
    if os.path.exists(generated):
        os.rename(generated, output_path)

    return output_path

# ---------------- HELPERS FOR MERGE ----------------
def to_pdf_if_needed(input_path, temp_dir):
    ext = Path(input_path).suffix.lower()
    if ext == '.pdf':
        return input_path
    # Convert to PDF
    pdf_path = os.path.join(temp_dir, Path(input_path).stem + '.pdf')
    conv_types = {
        '.docx': 'docx_to_pdf',
        '.txt': 'txt_to_pdf',
        '.pptx': 'pptx_to_pdf',
        '.jpg': 'image_to_pdf',
        '.jpeg': 'image_to_pdf',
        '.png': 'image_to_pdf',
    }
    ctype = conv_types.get(ext)
    if ctype:
        convert_file(input_path, ctype, pdf_path)
        return pdf_path
    raise ValueError(f"Cannot convert {ext} to PDF for merge")

def merge_pdfs(pdf_paths, output_path):
    master = fitz.open()
    for pdf_path in pdf_paths:
        doc = fitz.open(pdf_path)
        master.insert_pdf(doc)
        doc.close()
    master.save(output_path)
    master.close()
    return output_path

# ---------------- MAIN DISPATCHER ----------------
def convert_file(input_path, conv_type, output_path):
    if conv_type == "merge_to_pdf" and isinstance(input_path, list):
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_paths = [to_pdf_if_needed(p, temp_dir) for p in input_path]
            return merge_pdfs(pdf_paths, output_path)
    
    ext = Path(input_path).suffix.lower()


    if conv_type == "docx_to_pdf" and ext == ".docx":
        return docx_to_pdf(input_path, output_path)

    elif conv_type == "txt_to_pdf" and ext == ".txt":
        return txt_to_pdf(input_path, output_path)

    elif conv_type == "image_to_pdf" and ext in [".jpg", ".jpeg", ".png"]:
        return image_to_pdf(input_path, output_path)

    elif conv_type == "pptx_to_pdf" and ext == ".pptx":
        return pptx_to_pdf(input_path, output_path)

    elif conv_type == "pdf_to_docx" and ext == ".pdf":
        return pdf_to_docx(input_path, output_path)

    elif conv_type == "pdf_to_txt" and ext == ".pdf":
        return pdf_to_txt(input_path, output_path)

    elif conv_type == "pdf_to_pptx" and ext == ".pdf":
        return pdf_to_pptx(input_path, output_path)

    elif conv_type == "pdf_to_image" and ext == ".pdf":
        return pdf_to_image(input_path, output_path)

    else:
        raise ValueError(f"Unsupported: {ext} → {conv_type}")
