from flask import Flask, render_template, request, send_file
import os
from pdf2docx import Converter
from docx2pdf import convert
from PIL import Image
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
import pdfkit
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


# WORD → PDF
@app.route("/word_to_pdf", methods=["POST"])
def word_to_pdf():

    file = request.files["file"]

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    output_path = input_path.replace(".docx", ".pdf")

    convert(input_path, output_path)

    return send_file(output_path, as_attachment=True)


# IMAGE → PDF
@app.route("/image_to_pdf", methods=["POST"])
def image_to_pdf():

    file = request.files["file"]

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    image = Image.open(input_path)

    pdf_path = input_path.split(".")[0] + ".pdf"

    image.convert("RGB").save(pdf_path)

    return send_file(pdf_path, as_attachment=True)


# TEXT → PDF
@app.route("/text_to_pdf", methods=["POST"])
def text_to_pdf():

    file = request.files["file"]

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    pdf_path = input_path.replace(".txt", ".pdf")

    c = canvas.Canvas(pdf_path)

    with open(input_path) as f:

        lines = f.readlines()

    y = 800

    for line in lines:

        c.drawString(50, y, line)

        y -= 20

    c.save()

    return send_file(pdf_path, as_attachment=True)


# HTML → PDF
@app.route("/html_to_pdf", methods=["POST"])
def html_to_pdf():

    file = request.files["file"]

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    pdf_path = input_path.replace(".html", ".pdf")

    pdfkit.from_file(input_path, pdf_path)

    return send_file(pdf_path, as_attachment=True)


# PDF → WORD
@app.route("/pdf_to_word", methods=["POST"])
def pdf_to_word():

    file = request.files["file"]

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    output_path = input_path.replace(".pdf", ".docx")

    cv = Converter(input_path)

    cv.convert(output_path)

    cv.close()

    return send_file(output_path, as_attachment=True)


# PDF → TEXT
@app.route("/pdf_to_text", methods=["POST"])
def pdf_to_text():

    file = request.files["file"]

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    output_path = input_path.replace(".pdf", ".txt")

    reader = PdfReader(input_path)

    with open(output_path, "w") as f:

        for page in reader.pages:

            text = page.extract_text()

            if text:
                f.write(text)

    return send_file(output_path, as_attachment=True)


# PPT → PDF
@app.route("/ppt_to_pdf", methods=["POST"])
def ppt_to_pdf():

    file = request.files["file"]

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(input_path)

    subprocess.run([
        "soffice",
        "--headless",
        "--convert-to",
        "pdf",
        input_path,
        "--outdir",
        UPLOAD_FOLDER
    ])

    output_file = input_path.replace(".pptx", ".pdf")

    return send_file(output_file, as_attachment=True)


# PDF → PPT
@app.route("/pdf_to_ppt", methods=["POST"])
def pdf_to_ppt():

    file = request.files["file"]

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(input_path)

    subprocess.run([
        "soffice",
        "--headless",
        "--convert-to",
        "pptx",
        input_path,
        "--outdir",
        UPLOAD_FOLDER
    ])

    output_file = input_path.replace(".pdf", ".pptx")

    return send_file(output_file, as_attachment=True)


if __name__ == "__main__":

    app.run(debug=True)