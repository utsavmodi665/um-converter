import streamlit as st
from pathlib import Path
import tempfile
import os
from converter import convert_file
from PyPDF2 import PdfMerger
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Docuvy",
    page_icon="📄",
    layout="wide"
)

# ---------------- SAFE LOGO ----------------
if os.path.exists("logo.png"):
    st.image(Image.open("logo.png"), width=120)
else:
    st.title("📄 Docuvy")

st.markdown("### Convert & Merge Files Instantly")

st.divider()

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["✨ Convert", "🔗 Merge PDF"])

# ---------------- CONVERT ----------------
with tab1:
    uploaded_files = st.file_uploader(
        "Upload files",
        type=["pdf", "docx", "txt", "pptx", "jpg", "png", "jpeg"],
        accept_multiple_files=True
    )

    if uploaded_files:
        conv_type = st.selectbox("Select Conversion", [
            "To PDF",
            "PDF → DOCX",
            "PDF → TXT",
            "PDF → PPTX",
            "PDF → Image"
        ])

        if st.button("🚀 Convert", use_container_width=True):

            progress = st.progress(0)
            temp_files = []

            for i, file in enumerate(uploaded_files):

                # ✅ SAFE TEMP FILE
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.name).suffix) as tmp:
                    tmp.write(file.getbuffer())
                    input_path = tmp.name
                    temp_files.append(input_path)

                ext = Path(input_path).suffix.lower()

                try:
                    # -------- TO PDF --------
                    if conv_type == "To PDF":
                        conv_map = {
                            '.docx': 'docx_to_pdf',
                            '.txt': 'txt_to_pdf',
                            '.pptx': 'pptx_to_pdf',
                            '.jpg': 'image_to_pdf',
                            '.jpeg': 'image_to_pdf',
                            '.png': 'image_to_pdf'
                        }

                        ctype = conv_map.get(ext)
                        if not ctype:
                            st.error(f"{file.name}: Unsupported")
                            continue

                        output_path = input_path.rsplit('.', 1)[0] + '.pdf'

                    # -------- FROM PDF --------
                    elif conv_type == "PDF → DOCX" and ext == ".pdf":
                        ctype = "pdf_to_docx"
                        output_path = input_path.replace(".pdf", ".docx")

                    elif conv_type == "PDF → TXT" and ext == ".pdf":
                        ctype = "pdf_to_txt"
                        output_path = input_path.replace(".pdf", ".txt")

                    elif conv_type == "PDF → PPTX" and ext == ".pdf":
                        ctype = "pdf_to_pptx"
                        output_path = input_path.replace(".pdf", ".pptx")

                    elif conv_type == "PDF → Image" and ext == ".pdf":
                        ctype = "pdf_to_image"
                        output_path = input_path.replace(".pdf", "_page.png")

                    else:
                        st.error(f"{file.name}: Invalid conversion")
                        continue

                    result = convert_file(input_path, ctype, output_path)

                    st.success(f"✅ {file.name} converted")

                    # DOWNLOAD
                    if isinstance(result, list):
                        for r in result:
                            with open(r, "rb") as f:
                                st.download_button(f"⬇️ {Path(r).name}", f, Path(r).name)
                    else:
                        with open(result, "rb") as f:
                            st.download_button(f"⬇️ Download", f, Path(result).name)

                except Exception as e:
                    st.error(f"{file.name}: {e}")

                progress.progress((i + 1) / len(uploaded_files))

            # CLEANUP
            for f in temp_files:
                if os.path.exists(f):
                    os.remove(f)

# ---------------- MERGE ----------------
with tab2:
    uploaded_files = st.file_uploader(
        "Upload files to merge (PDF only)",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files and len(uploaded_files) > 1:

        if st.button("🔗 Merge PDF", use_container_width=True):

            temp_files = []
            merger = PdfMerger()

            try:
                for file in uploaded_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(file.getbuffer())
                        temp_files.append(tmp.name)
                        merger.append(tmp.name)

                output_path = "merged_docuvy.pdf"
                merger.write(output_path)
                merger.close()

                st.success("✅ Merged successfully!")

                with open(output_path, "rb") as f:
                    st.download_button("⬇️ Download Merged PDF", f, output_path)

            except Exception as e:
                st.error(f"Merge failed: {e}")

            # CLEANUP
            for f in temp_files:
                if os.path.exists(f):
                    os.remove(f)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Docuvy • Fast, Clean File Conversion 🚀")
