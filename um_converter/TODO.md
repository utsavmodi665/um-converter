# UM Converter Streamlit Migration TODO

## Step 1: Create requirements.txt [DONE]
- List all dependencies: streamlit, pymupdf, pdf2docx, python-docx, pillow, reportlab, pypandoc, docx2pdf, pypdf2.

## Step 2: Create utils.py [DONE]
- File validation (size, ext), auto naming, batch processing, tempfile management, cleanup.

## Step 3: Create converter.py [DONE]
- Modular functions: docx_to_pdf(), pdf_to_docx(), image_to_pdf(), pdf_to_image(), txt_to_pdf(), pdf_to_txt(), pptx_to_pdf(), pdf_to_pptx() etc., with error handling.

## Step 4: Create main.py [DONE]
- Streamlit app: sidebar theme toggle, file uploader (multi), conversion selectbox, progress bar, preview, batch download zip.

## Step 5: Install deps [DONE]
- pip install -r requirements.txt

## Step 6: Test [DONE]
- Single/batch conversions with uploads/ samples.

## Step 7: Run [DONE]
- streamlit run main.py

## Step 8: Cleanup [DONE]
- Removed old Flask files.
