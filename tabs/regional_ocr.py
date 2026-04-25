# ============================================================
# Vidhi-AI | Tab 5: Regional OCR (Vernacular Evidence)
# ============================================================

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils import html_escape
from vidhi_logger import logger

# Import Ollama
try:
    from langchain_community.llms import Ollama
except ImportError:
    from langchain_ollama import OllamaLLM as Ollama

# OCR dependencies
import pytesseract
from pdf2image import convert_from_bytes


def render():
    """Render the Vernacular Evidence Processing tab."""
    st.markdown(
        '<div class="section-header">Vernacular Evidence Processing</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="info-label">Upload a regional-language PDF document '
        '(Kannada, Hindi, Marathi, or English). The system uses an '
        'OCR-First approach: every page is converted to a high-resolution '
        'image and processed through Tesseract OCR with regional language '
        'packs. This eliminates (cid:xxxx) encoding issues. The extracted '
        'text is then translated into formal English using the local '
        'Llama-3 model. No data leaves this machine.</p>',
        unsafe_allow_html=True,
    )

    # Supported languages badge row
    st.markdown(
        '<div>'
        '<span class="lang-info-badge">Kannada</span>'
        '<span class="lang-info-badge">Hindi</span>'
        '<span class="lang-info-badge">Marathi</span>'
        '<span class="lang-info-badge">English</span>'
        '<span class="lang-info-badge">OCR-First Pipeline</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    regional_file = st.file_uploader(
        "Upload Regional Language PDF",
        type=["pdf"],
        key="regional_pdf_uploader",
    )

    run_translate = st.button(
        "Analyze & Translate Evidence",
        use_container_width=True,
        key="btn_translate",
    )

    if run_translate:
        if regional_file is None:
            st.warning(
                "Please upload a PDF document before initiating "
                "translation."
            )
        else:
            with st.spinner("Analyzing Regional Dialects..."):
                extracted_text = ""
                pdf_bytes = regional_file.read()

                # --- Step 1: OCR-First — convert every page to image ---
                try:
                    images = convert_from_bytes(
                        pdf_bytes, dpi=300, fmt="png"
                    )

                    for page_num, page_img in enumerate(images, 1):
                        ocr_text = pytesseract.image_to_string(
                            page_img, lang="kan+hin+mar+eng"
                        )
                        if ocr_text and ocr_text.strip():
                            extracted_text += (
                                f"--- Page {page_num} ---\n"
                                f"{ocr_text.strip()}\n\n"
                            )

                except FileNotFoundError as e:
                    logger.error("Poppler/Tesseract not found: %s", e)
                    st.error(
                        "PDF-to-image conversion requires Poppler. "
                        "Please install Poppler for Windows:\n\n"
                        "1. Download from: "
                        "https://github.com/oschwartz10612/poppler-windows/releases\n"
                        "2. Extract and add the 'bin' folder to "
                        "your system PATH.\n"
                        "3. Restart this application."
                    )
                except Exception as e:
                    error_msg = str(e)
                    logger.error("OCR extraction failed: %s", error_msg)
                    if "poppler" in error_msg.lower():
                        st.error(
                            "PDF-to-image conversion requires Poppler. "
                            "Please install Poppler for Windows:\n\n"
                            "1. Download from: "
                            "https://github.com/oschwartz10612/poppler-windows/releases\n"
                            "2. Extract and add the 'bin' folder to "
                            "your system PATH.\n"
                            "3. Restart this application."
                        )
                    else:
                        st.error(
                            f"OCR extraction failed: {error_msg}. "
                            "Ensure Tesseract OCR is installed with "
                            "the 'kan', 'hin', 'mar', 'eng' language "
                            "packs, and Poppler is available on PATH."
                        )

                if not extracted_text.strip():
                    st.error(
                        "No text could be extracted from the uploaded "
                        "document. Possible causes:\n\n"
                        "1. Poppler is not installed or not on PATH.\n"
                        "2. Tesseract OCR is not installed.\n"
                        "3. Regional language packs (kan, hin, mar) "
                        "are not installed for Tesseract.\n"
                        "4. The PDF may be empty or corrupt."
                    )
                else:
                    # --- Step 2: Translate via Llama-3 ---
                    translate_llm = Ollama(
                        model="llama3",
                        temperature=0,
                        num_predict=4096,
                    )

                    translate_prompt = ChatPromptTemplate.from_messages([
                        (
                            "system",
                            "You are a Senior Judicial Translator. "
                            "Translate the following text into formal "
                            "English. Do not redact or replace names of "
                            "people, cities, or specific locations. You "
                            "must include the original names like "
                            "'Gangadhar V' and 'Hirandahalli' in the "
                            "English report.\n\n"
                            "Rules:\n"
                            "1. Preserve ALL proper nouns -- person names, "
                            "place names, city names, village names, "
                            "street names, and organization names -- "
                            "exactly as written in the source text. "
                            "Never replace them with placeholders like "
                            "[Name] or [City] or [Location].\n"
                            "2. Preserve all dates, numbers, registration "
                            "numbers, phone numbers, and case references "
                            "exactly as they appear.\n"
                            "3. Mark any untranslatable or unclear words "
                            "in [brackets] with a note.\n"
                            "4. Use formal legal English throughout.\n"
                            "5. Structure the output as a 'Judicial "
                            "Translation Report' with clear sections.\n"
                            "6. Do not add information not present in "
                            "the source text.\n"
                            "7. No emojis. No casual language.",
                        ),
                        ("human", "{regional_text}"),
                    ])

                    translate_chain = (
                        translate_prompt
                        | translate_llm
                        | StrOutputParser()
                    )

                    translated_text = translate_chain.invoke(
                        {"regional_text": extracted_text}
                    )
                    logger.info("Regional OCR translation completed.")

                    # --- Step 3: Side-by-side display ---
                    st.markdown(
                        '<div class="section-header"'
                        ' style="margin-top:1.5rem;">'
                        'Translation Results</div>',
                        unsafe_allow_html=True,
                    )

                    col_original, col_translated = st.columns(2)

                    with col_original:
                        safe_original = html_escape(extracted_text)
                        st.markdown(
                            '<div class="lang-column-header">'
                            'Original Extracted Text (OCR)</div>'
                            f'<div class="lang-text-box">'
                            f'{safe_original}</div>',
                            unsafe_allow_html=True,
                        )

                    with col_translated:
                        safe_translated = html_escape(translated_text)
                        st.markdown(
                            '<div class="lang-column-header">'
                            'English Translation</div>'
                            f'<div class="lang-text-box">'
                            f'{safe_translated}</div>',
                            unsafe_allow_html=True,
                        )
