# ============================================================
# Vidhi-AI | Tab 3: Conflict Detection
# ============================================================

import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from vidhi_logger import logger

# Import Ollama
try:
    from langchain_community.llms import Ollama
except ImportError:
    from langchain_ollama import OllamaLLM as Ollama


def render():
    """Render the Evidence Conflict Detection tab."""
    st.markdown(
        '<div class="section-header">Evidence Conflict Detection</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="info-label">This module performs a judicial audit across '
        'selected legal documents. The system compares witness statements, '
        'FIRs, and other records to identify contradictions in timelines, '
        'vehicle descriptions, suspect behavior, and evidentiary details. '
        'Select exactly the documents you want to compare below.</p>',
        unsafe_allow_html=True,
    )

    # Build available document list from uploads + disk fallback
    _all_conflict_docs = st.session_state.get("all_pdf_texts", {})
    if not _all_conflict_docs:
        for _fb_name in ["dummy_fir.pdf", "witness_statement.pdf"]:
            if os.path.exists(_fb_name):
                _fb_loader = PyPDFLoader(_fb_name)
                _fb_pages = _fb_loader.load()
                _all_conflict_docs[_fb_name] = "\n".join(
                    p.page_content for p in _fb_pages
                )

    _available_doc_names = list(_all_conflict_docs.keys())

    if _available_doc_names:
        selected_conflict_docs = st.multiselect(
            "Select documents to compare:",
            options=_available_doc_names,
            default=_available_doc_names,
            help="Pick at least 2 documents. De-select any you don't need to stay within the LLM context window.",
            key="conflict_doc_selector",
        )
    else:
        selected_conflict_docs = []

    run_conflict = st.button(
        "Scan for Evidence Conflicts",
        use_container_width=True,
        key="btn_conflict",
    )

    if run_conflict:
        # Use only the user-selected documents
        conflict_texts = {
            k: v for k, v in _all_conflict_docs.items()
            if k in selected_conflict_docs
        }

        if len(conflict_texts) < 2:
            st.warning(
                "At least two documents are required for conflict detection. "
                "Please upload multiple PDFs."
            )
        else:
            with st.spinner(
                "Judicial Auditor is scanning for evidentiary conflicts..."
            ):
                # Use temperature=0 for deterministic, reproducible results
                conflict_llm = Ollama(
                    model="llama3",
                    temperature=0,
                    num_predict=2048,
                )

                # Build combined text with document labels
                combined_text = ""
                doc_names_ordered = []
                for doc_name, doc_text in conflict_texts.items():
                    doc_names_ordered.append(doc_name)
                    combined_text += (
                        f"\n{'='*60}\n"
                        f"DOCUMENT: {doc_name}\n"
                        f"{'='*60}\n"
                        f"{doc_text}\n"
                    )

                # Warn if text is very long
                if len(combined_text) > 24000:
                    st.warning(
                        f"Combined document text is {len(combined_text):,} characters. "
                        "This may exceed the LLM context window. Consider de-selecting "
                        "some documents for more accurate results."
                    )

                conflict_prompt = ChatPromptTemplate.from_messages([
                    (
                        "system",
                        "You are a Judicial Auditor conducting a mandatory "
                        "evidentiary cross-examination. You MUST perform an "
                        "exhaustive line-by-line comparison of ALL provided "
                        "documents. This is a court-ordered review.\n\n"
                        "MANDATORY COMPARISON CHECKLIST -- you must check "
                        "each of these categories:\n"
                        "a) Date and time of incident\n"
                        "b) Location / place of incident\n"
                        "c) Vehicle make, model, color, registration number\n"
                        "d) Suspect physical description (height, build, "
                        "clothing, distinguishing marks)\n"
                        "e) Suspect behavior and actions\n"
                        "f) Sequence and chronology of events\n"
                        "g) Witness identity and role\n"
                        "h) Any other factual claims\n\n"
                        "RULES:\n"
                        "1. If ANY detail in one document differs from "
                        "another document even slightly, it IS a conflict. "
                        "Report it.\n"
                        "2. For EACH conflict found, output EXACTLY in this "
                        "format (do not deviate):\n"
                        "CONFLICT: [Brief title of the contradiction]\n"
                        "DOCUMENT A: [Exact quote or detail from first "
                        "document, citing the document name]\n"
                        "DOCUMENT B: [Exact quote or detail from second "
                        "document, citing the document name]\n"
                        "SEVERITY: [CRITICAL / MODERATE / MINOR]\n"
                        "---\n"
                        "3. After ALL conflicts, write a section starting "
                        "with the line:\nJUDICIAL OBSERVATIONS\n"
                        "followed by a brief summary of overall document "
                        "reliability.\n"
                        "4. ONLY if there are truly ZERO factual differences "
                        "across ALL categories above, write exactly: "
                        "NO DISCREPANCIES DETECTED\n"
                        "5. Do not add pleasantries, preamble, or extra "
                        "conversation. No emojis. Formal legal language "
                        "only.\n"
                        "6. You must output at least one CONFLICT or the "
                        "exact phrase NO DISCREPANCIES DETECTED. There is "
                        "no third option.",
                    ),
                    ("human", "{documents}"),
                ])

                conflict_chain = (
                    conflict_prompt | conflict_llm | StrOutputParser()
                )

                conflict_report = conflict_chain.invoke(
                    {"documents": combined_text}
                )
                logger.info("Conflict detection completed for %d documents.", len(conflict_texts))

            # Determine if conflicts were found (robust detection)
            report_upper = conflict_report.upper()
            no_conflict_phrases = [
                "NO DISCREPANCIES DETECTED",
                "NO CONTRADICTIONS",
                "NO CONFLICTS",
                "NO DISCREPANCIES FOUND",
                "NO EVIDENTIARY CONFLICTS",
                "DOCUMENTS ARE CONSISTENT",
                "NO MATERIAL DIFFERENCES",
            ]
            explicitly_clean = any(
                phrase in report_upper for phrase in no_conflict_phrases
            )
            has_conflict_markers = (
                "CONFLICT:" in report_upper
                or "DOCUMENT A:" in report_upper
                or "SEVERITY:" in report_upper
            )
            has_conflicts = has_conflict_markers and not explicitly_clean

            # Status Banner
            if has_conflicts:
                st.markdown(
                    '<div class="audit-banner-red">'
                    'DISCREPANCIES DETECTED -- Judicial Review Required'
                    '</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="audit-banner-green">'
                    'No Discrepancies Detected -- Documents Consistent'
                    '</div>',
                    unsafe_allow_html=True,
                )

            # Document list
            doc_list = ", ".join(conflict_texts.keys())
            st.markdown(
                f'<p class="info-label"><strong>Documents Analyzed:</strong> '
                f'{doc_list}</p>',
                unsafe_allow_html=True,
            )

            # Parse and display structured report
            if has_conflicts:
                # Split report into conflict blocks
                lines = conflict_report.split("\n")
                current_conflict = []
                conflicts_list = []
                observations = []
                in_observations = False

                for line in lines:
                    stripped = line.strip()
                    if stripped.upper().startswith("JUDICIAL OBSERVATIONS"):
                        if current_conflict:
                            conflicts_list.append(
                                "\n".join(current_conflict)
                            )
                            current_conflict = []
                        in_observations = True
                        continue
                    if in_observations:
                        if stripped:
                            observations.append(stripped)
                        continue
                    if stripped.upper().startswith("CONFLICT"):
                        if current_conflict:
                            conflicts_list.append(
                                "\n".join(current_conflict)
                            )
                        current_conflict = [stripped]
                    elif stripped == "---":
                        if current_conflict:
                            conflicts_list.append(
                                "\n".join(current_conflict)
                            )
                            current_conflict = []
                    elif stripped:
                        current_conflict.append(stripped)

                if current_conflict:
                    conflicts_list.append("\n".join(current_conflict))

                # Render audit report
                st.markdown(
                    '<div class="audit-report">'
                    '<div class="audit-report-title">'
                    'Formal Conflict Analysis Report</div>',
                    unsafe_allow_html=True,
                )

                # Render each conflict as a red-highlighted block
                for idx, conflict_block in enumerate(conflicts_list, 1):
                    safe_block = (
                        conflict_block
                        .replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
                    )
                    for label in [
                        "CONFLICT:", "DOCUMENT A:", "DOCUMENT B:",
                        "SEVERITY:",
                    ]:
                        safe_block = safe_block.replace(
                            label, f"<strong>{label}</strong>"
                        )
                    safe_block = safe_block.replace("\n", "<br>")

                    st.markdown(
                        f'<div class="conflict-label">'
                        f'Finding #{idx}</div>'
                        f'<div class="conflict-item">{safe_block}</div>',
                        unsafe_allow_html=True,
                    )

                # Judicial Observations
                if observations:
                    obs_text = " ".join(observations)
                    st.markdown(
                        f'<div class="section-header" '
                        f'style="margin-top:1.5rem;">'
                        f'Judicial Observations</div>'
                        f'<div class="observation-box">{obs_text}</div>',
                        unsafe_allow_html=True,
                    )

                st.markdown('</div>', unsafe_allow_html=True)

            else:
                # No conflicts - show clean report
                st.markdown(
                    '<div class="audit-report">'
                    '<div class="audit-report-title">'
                    'Formal Conflict Analysis Report</div>'
                    '<p style="text-align:center; font-size:1.1rem; '
                    'color:#1B5E20 !important; font-weight:600;">'
                    'All documents have been cross-referenced. No '
                    'evidentiary contradictions were identified. '
                    'The records appear internally consistent.</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )
