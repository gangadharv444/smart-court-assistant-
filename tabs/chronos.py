# ============================================================
# Vidhi-AI | Tab 2: Chronos (Timeline Extraction)
# ============================================================

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from loaders import load_llm
from vidhi_logger import logger


def render():
    """Render the Chronos Evidence Timeline tab."""
    st.markdown(
        '<div class="section-header">Chronos Evidence Timeline</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="info-label">Extract a strict chronological timeline of all events '
        'from the selected legal documents.</p>',
        unsafe_allow_html=True,
    )

    # Document selector for Chronos
    _chrono_docs = st.session_state.get("all_pdf_texts", {})
    _chrono_doc_names = list(_chrono_docs.keys())

    if _chrono_doc_names:
        selected_chronos_docs = st.multiselect(
            "Select documents for timeline extraction:",
            options=_chrono_doc_names,
            default=_chrono_doc_names,
            help="Choose which uploaded PDFs to extract the timeline from.",
            key="chronos_doc_selector",
        )
    else:
        selected_chronos_docs = []

    run_chronos = st.button(
        "Extract Timeline",
        use_container_width=True,
        key="btn_chronos",
    )

    if run_chronos:
        # Build text from selected documents
        if selected_chronos_docs and _chrono_docs:
            text_to_process = "\n\n".join(
                _chrono_docs[d] for d in selected_chronos_docs
                if d in _chrono_docs
            )
        else:
            text_to_process = st.session_state.get("pdf_text", "")

        if not text_to_process:
            st.warning(
                "No document available. Please upload a PDF first."
            )

        if text_to_process:
            with st.spinner(
                "Chronos is extracting the evidence timeline..."
            ):
                llm = load_llm()

                chronos_prompt = ChatPromptTemplate.from_messages([
                    (
                        "system",
                        "You are an expert legal data extractor. "
                        "Read the provided text and extract a strict, "
                        "chronological timeline of all events. "
                        "Format the output as a bulleted list with the "
                        "Date/Time followed by the Event. "
                        "Do not add any extra conversation.",
                    ),
                    ("human", "{text}"),
                ])

                chronos_chain = (
                    chronos_prompt | llm | StrOutputParser()
                )

                timeline = chronos_chain.invoke({"text": text_to_process})
                logger.info("Chronos timeline extraction completed.")

            st.markdown(
                '<div class="section-header">Extracted Timeline</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="result-card">{timeline}</div>',
                unsafe_allow_html=True,
            )
