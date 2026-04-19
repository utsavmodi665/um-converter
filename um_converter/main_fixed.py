import streamlit as st
from converter import convert_file
from utils import validate_file, save_uploaded_files, create_zip, cleanup_files
from pathlib import Path

st.set_page_config(page_title="UM Converter", page_icon="🔄", layout="wide")

# Theme toggle
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

st.sidebar.title("⚙️ Settings")
if st.sidebar.button("🌙 Dark" if not st.session_state.dark_mode else "☀️ Light"):
    st.session_state.dark_mode = not st.session_state.dark_mode
st.sidebar.markdown("---")

# Apply theme
if st.session_state.dark_mode:
    st.markdown("""
    <style>
        .stApp { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔄 UM Converter")
st.markdown("**Universal File Converter** - DOCX, TXT, PPTX, Images ↔ PDF")

# File uploader
uploaded_files = st.file_uploader("Choose files", 
    type=['docx', 'pdf', 'txt', 'pptx', 'png', 'jpg', 'jpeg'], 
    accept_multiple_files=True)

if uploaded_files:
    valid_files = []
    for f in uploaded_files:
        ok, msg = validate_file(f)
        if ok:
            valid_files.append(f)
        else:
            st.warning(msg)

    if valid_files:
        conv_options = ["To PDF", "PDF to DOCX", "PDF to TXT", "PDF to PPTX", "PDF to Image"]
        conv_type = st.selectbox("Select conversion:", conv_options)

        if st.button("🚀 Convert", type="primary"):
            with st.spinner('Processing...'):
                saved_paths = save_uploaded_files(valid_files)
                output_paths = []
                progress_bar = st.progress(0)
                
                for i, input_path in enumerate(saved_paths):
                    try:
                        # Map UI option to converter
                        if conv_type == "To PDF":
                            ctype = 'to_pdf'
                        elif conv_type == "PDF to DOCX":
                            ctype = 'pdf_to_docx'
                        elif conv_type == "PDF to TXT":
                            ctype = 'pdf_to_txt'
                        elif conv_type == "PDF to PPTX":
                            ctype = 'pdf_to_pptx'
                        elif conv_type == "PDF to Image":
                            ctype = 'pdf_to_image'
                        
                        output_path = convert_file(input_path, ctype)
                        output_paths.append(output_path)
                    except Exception as e:
                        st.error(f"Failed {Path(input_path).name}: {e}")
                    
                    progress_bar.progress((i+1)/len(saved_paths))

                if output_paths:
                    st.success(f"✅ Converted {len(output_paths)} files!")
                    
                    # Preview & Download
                    for op in output_paths:
                        with open(op, "rb") as f:
                            st.download_button(
                                label=f"Download {Path(op).name}",
                                data=f,
                                file_name=Path(op).name,
                                mime="application/octet-stream"
                            )
                    
                    # Batch ZIP
                    if len(output_paths) > 1:
                        zip_path = "converted_files.zip"
                        create_zip(output_paths, zip_path)
                        with open(zip_path, "rb") as zf:
                            st.download_button(
                                "📦 Download All (ZIP)",
                                zf,
                                zip_path
                            )
                        # Cleanup ZIP
                        os.remove(zip_path)
                
                # Cleanup inputs
                cleanup_files(saved_paths)

# Info
with st.expander("ℹ️ Info"):
    st.markdown("""
    **Supported conversions:**
    - **To PDF**: DOCX, TXT, PPTX, JPG/PNG 
    - **From PDF**: DOCX, TXT, PPTX, Images
    
    **Notes:**
    - PPT conversions require LibreOffice installed
    - Max file size: 50MB
    - Batch processing supported
    """)

st.markdown("---")
st.markdown("*UM Converter v1.0 - Production Ready*")

