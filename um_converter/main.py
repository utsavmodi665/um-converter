import streamlit as st
from pathlib import Path
import os
from converter import convert_file

st.set_page_config(page_title="UM Converter", layout="wide")

st.title("🔄 UM Converter")

uploaded_files = st.file_uploader(
    "Upload Files",
    type=["pdf", "docx", "txt", "pptx", "jpg", "png", "jpeg"],
    accept_multiple_files=True
)

conv_type = st.selectbox("Select Conversion", [
    "To PDF",
    "PDF → DOCX",
    "PDF → TXT",
    "PDF → PPTX",
    "PDF → Image"
])

if uploaded_files and st.button("🚀 Convert"):

    progress = st.progress(0)

    for i, file in enumerate(uploaded_files):

        input_path = file.name
        with open(input_path, "wb") as f:
            f.write(file.getbuffer())

        ext = Path(input_path).suffix.lower()

        try:
            # -------- TO PDF --------
            if conv_type == "To PDF":
                if ext == ".docx":
                    ctype = "docx_to_pdf"
                    output = input_path.replace(".docx", ".pdf")
                elif ext == ".txt":
                    ctype = "txt_to_pdf"
                    output = input_path.replace(".txt", ".pdf")
                elif ext in [".jpg", ".jpeg", ".png"]:
                    ctype = "image_to_pdf"
                    output = input_path.rsplit(".",1)[0] + ".pdf"
                elif ext == ".pptx":
                    ctype = "pptx_to_pdf"
                    output = input_path.replace(".pptx", ".pdf")
                else:
                    st.error(f"{file.name}: Unsupported")
                    continue

            # -------- FROM PDF --------
            elif conv_type == "PDF → DOCX" and ext == ".pdf":
                ctype = "pdf_to_docx"
                output = input_path.replace(".pdf", ".docx")

            elif conv_type == "PDF → TXT" and ext == ".pdf":
                ctype = "pdf_to_txt"
                output = input_path.replace(".pdf", ".txt")

            elif conv_type == "PDF → PPTX" and ext == ".pdf":
                ctype = "pdf_to_pptx"
                output = input_path.replace(".pdf", ".pptx")

            elif conv_type == "PDF → Image" and ext == ".pdf":
                ctype = "pdf_to_image"
                output = input_path.replace(".pdf", ".png")

            else:
                st.error(f"{file.name}: Invalid conversion")
                continue

            result = convert_file(input_path, ctype, output)

            st.success(f"✅ Converted: {file.name}")

            # Multiple images support
            if isinstance(result, list):
                for r in result:
                    with open(r, "rb") as f:
                        st.download_button(f"Download {Path(r).name}", f, Path(r).name)
            else:
                with open(result, "rb") as f:
                    st.download_button(f"Download {Path(result).name}", f, Path(result).name)

        except Exception as e:
            st.error(f"{file.name}: {e}")

        progress.progress((i + 1) / len(uploaded_files))

st.markdown("---")
st.caption("UM Converter • FINAL WORKING VERSION 🚀")
