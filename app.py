# ============================================================
# Vidhi-AI | Smart Court Assistant Dashboard
# 100% Offline · Zero Cloud APIs · Air-Gapped Courtroom
# ============================================================

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import warnings

from styles import inject_css
from utils import sanitize_filename, get_upload_dir
from loaders import check_ollama_health
from vidhi_logger import logger
from tabs import case_analysis, chronos, conflict, statute_bridge, regional_ocr, bulk_analysis

warnings.filterwarnings("ignore")

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Smart Court Assistant",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# INJECT GOVERNMENT-STYLE THEME (CSS)
# =============================================================================
inject_css()

# =============================================================================
# OLLAMA HEALTH CHECK (on first run only)
# =============================================================================
if "ollama_checked" not in st.session_state:
    st.session_state["ollama_checked"] = True
    if not check_ollama_health():
        st.warning(
            "⚠️ Ollama server is not running on localhost:11434. "
            "AI-powered features (Case Analysis, Chronos, Conflict Detection, "
            "AI Interpretation) will not work until Ollama is started.\n\n"
            "Run: `ollama serve` in a separate terminal."
        )

# =============================================================================
# HEADER
# =============================================================================
st.markdown("""
<div class="govt-header">
    <div style="font-size:2.1rem; font-weight:700; letter-spacing:2px; color:#FFFFFF !important; text-shadow:1px 1px 4px rgba(0,0,0,0.6); margin:0; font-family:'Segoe UI',sans-serif;">Smart Court Assistant</div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# LAYOUT: LEFT CONTROL PANEL | RIGHT CONTENT AREA
# =============================================================================
col_control, col_main = st.columns([1, 2])

# -----------------------------------------------------------------------------
# LEFT COLUMN — Control Panel
# -----------------------------------------------------------------------------
with col_control:
    st.markdown('<div class="section-header">Document Control Panel</div>',
                unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload Legal Documents (PDF)",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload FIRs, chargesheets, witness statements, or any legal PDFs for analysis.",
    )

    # Process uploaded files
    all_pdf_texts = {}
    all_chunks = []
    total_pages = 0
    total_chunks = 0

    if uploaded_files:
        upload_dir = get_upload_dir()

        for uploaded_file in uploaded_files:
            safe_name = sanitize_filename(uploaded_file.name)
            temp_path = os.path.join(upload_dir, safe_name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            try:
                loader = PyPDFLoader(temp_path)
                pages = loader.load()
                page_count = len(pages)
                total_pages += page_count
                pdf_text = "\n".join(page.page_content for page in pages)
                all_pdf_texts[uploaded_file.name] = pdf_text

                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500, chunk_overlap=50
                )
                chunks = splitter.split_documents(pages)
                all_chunks.extend(chunks)
                total_chunks += len(chunks)
            except Exception as e:
                logger.error("Failed to process %s: %s", uploaded_file.name, e)
                st.error(f"Failed to process {uploaded_file.name}: {e}")

        st.markdown(
            '<div class="status-badge">DOCUMENTS LOADED</div>',
            unsafe_allow_html=True,
        )
        for fname in all_pdf_texts:
            st.markdown(f'<p class="info-label"><strong>File:</strong> {fname}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="info-label"><strong>Total Files:</strong> {len(uploaded_files)}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="info-label"><strong>Total Pages:</strong> {total_pages}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="info-label"><strong>Total Chunks:</strong> {total_chunks}</p>', unsafe_allow_html=True)

        # Store in session state
        file_names_key = "|".join(sorted(f.name for f in uploaded_files))
        if st.session_state.get("file_names_key") != file_names_key:
            st.session_state["chunks"] = all_chunks
            st.session_state["all_pdf_texts"] = all_pdf_texts
            st.session_state["pdf_text"] = "\n\n".join(all_pdf_texts.values())
            st.session_state["file_names_key"] = file_names_key
    else:
        # Fallback: use existing vault
        if os.path.exists("./vidhi_vault"):
            st.markdown(
                '<div class="status-badge">VAULT CONNECTED</div>',
                unsafe_allow_html=True,
            )
            st.markdown('<p class="info-label">Using pre-built evidence vault.</p>', unsafe_allow_html=True)
        else:
            st.info("Upload a PDF to begin analysis.")

    # System status
    st.markdown("")
    st.markdown('<div class="section-header">Dashboard Ready</div>',
                unsafe_allow_html=True)
    st.markdown('<p class="info-label" style="text-align: center;">Verified Secure Local Environment.</p>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# RIGHT COLUMN — Main Content Area with Tabs
# -----------------------------------------------------------------------------
with col_main:
    tab_case, tab_chronos, tab_conflict, tab_statute, tab_regional, tab_bulk = st.tabs(
        ["Case Analysis", "Chronos", "Conflict",
         "IPC to BNS", "Regional OCR",
         "Bulk Analysis"]
    )

    with tab_case:
        case_analysis.render()

    with tab_chronos:
        chronos.render()

    with tab_conflict:
        conflict.render()

    with tab_statute:
        statute_bridge.render()

    with tab_regional:
        regional_ocr.render()

    with tab_bulk:
        bulk_analysis.render()

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("""
<div class="govt-footer">
    Smart Court Assistant |
    Secure Air-Gapped Deployment | All processing is 100% local — zero cloud API calls
</div>
""", unsafe_allow_html=True)
