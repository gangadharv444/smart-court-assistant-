# ============================================================
# Vidhi-AI | Tab 6: Bulk Document Analysis
# ============================================================

import re
import io
import streamlit as st
import pdfplumber
from loaders import load_bns_csv_rows
from ipc_bns_mapping import IPC_TO_BNS, lookup_ipc_to_bns, get_ipc_section_name
from utils import clean_ai_output, html_escape
from vidhi_logger import logger

# Import Ollama
try:
    from langchain_community.llms import Ollama
except ImportError:
    from langchain_ollama import OllamaLLM as Ollama


def render():
    """Render the Bulk Document Analysis tab."""
    st.markdown(
        '<div class="section-header">'
        'Bulk Document Analysis — IPC → BNS Transition Scanner'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#2C3E50; font-size:0.95rem; '
        'margin-bottom:1.2rem;">'
        'Upload any legal PDF (FIR, charge sheet, judgment, '
        'petition). The system automatically extracts text, '
        'identifies <strong>every IPC section reference</strong>, '
        'maps each one to its BNS equivalent using the local '
        'deterministic dictionary, retrieves full BNS descriptions '
        'from the database, and generates a comprehensive '
        'AI-powered transition analysis — all 100% offline.'
        '</p>',
        unsafe_allow_html=True,
    )

    bulk_pdf = st.file_uploader(
        "Upload Legal Document (PDF)",
        type=["pdf"],
        key="bulk_pdf_uploader",
        help="Supports FIRs, charge sheets, judgments, "
             "petitions, police reports, etc.",
    )

    if bulk_pdf is not None:
        run_bulk = st.button(
            "Scan Document for IPC → BNS Transitions",
            use_container_width=True,
            key="bulk_scan_btn",
        )

        if run_bulk:
            # ── PHASE 1: PDF Text Extraction ────────────────
            with st.spinner(
                "Phase 1/4 — Extracting text from PDF..."
            ):
                pdf_bytes = bulk_pdf.read()
                extracted_pages = []

                try:
                    # Primary: pdfplumber
                    pdf_stream = io.BytesIO(pdf_bytes)
                    with pdfplumber.open(pdf_stream) as pdf:
                        for i, page in enumerate(pdf.pages):
                            page_text = page.extract_text()
                            if page_text and page_text.strip():
                                extracted_pages.append({
                                    "page": i + 1,
                                    "text": page_text.strip(),
                                })
                except (ValueError, TypeError) as e:
                    logger.warning("pdfplumber failed: %s", e)
                    extracted_pages = []

                # Fallback: PyMuPDF (fitz) if pdfplumber fails
                if not extracted_pages:
                    try:
                        import fitz
                        pdf_doc = fitz.open(
                            stream=pdf_bytes, filetype="pdf"
                        )
                        for i in range(len(pdf_doc)):
                            page_text = pdf_doc[i].get_text()
                            if page_text and page_text.strip():
                                extracted_pages.append({
                                    "page": i + 1,
                                    "text": page_text.strip(),
                                })
                        pdf_doc.close()
                    except (ImportError, ValueError) as e:
                        logger.warning("PyMuPDF fallback failed: %s", e)
                        extracted_pages = []

                if not extracted_pages:
                    st.error(
                        "Could not extract text from this PDF. "
                        "The file may be scanned/image-based. "
                        "Try using the Regional Language Support "
                        "tab for OCR-based extraction."
                    )
                    st.stop()

                full_text = "\n\n".join(
                    p["text"] for p in extracted_pages
                )
                total_pages = len(extracted_pages)
                total_chars = len(full_text)

                st.markdown(
                    '<div class="audit-banner-green">'
                    f'TEXT EXTRACTED — {total_pages} PAGE(S), '
                    f'{total_chars:,} CHARACTERS'
                    '</div>',
                    unsafe_allow_html=True,
                )

            # ── PHASE 2: IPC Section Identification ─────────
            with st.spinner(
                "Phase 2/4 — Scanning for IPC section "
                "references..."
            ):
                # Comprehensive regex patterns for IPC refs
                ipc_patterns = [
                    # "Section 302", "Sec. 420", "Sec 378"
                    r'[Ss]ec(?:tion)?\.?\s*(\d+[A-Za-z]*)',
                    # "u/s 302", "U/S 420", "u/s. 302"
                    r'[Uu]/[Ss]\.?\s*(\d+[A-Za-z]*)',
                    # "IPC 302", "I.P.C. 420", "IPC Section 302"
                    r'I\.?P\.?C\.?\s*(?:[Ss]ec(?:tion)?\.?\s*)?'
                    r'(\d+[A-Za-z]*)',
                    # "302 IPC", "420 I.P.C."
                    r'(\d+[A-Za-z]*)\s*I\.?P\.?C\.?',
                    # "Section 302/307/34" (slash-separated)
                    r'[Ss]ec(?:tion)?\.?\s*(\d+[A-Za-z]*)'
                    r'(?:\s*/\s*(\d+[A-Za-z]*))*',
                    # "Sections 302, 307, and 34"
                    r'[Ss]ections?\s+(\d+[A-Za-z]*)'
                    r'(?:\s*,\s*(\d+[A-Za-z]*))*',
                    # "S. 302" (abbreviated)
                    r'\bS\.\s*(\d+[A-Za-z]*)',
                ]

                found_ipc_sections = set()

                for pattern in ipc_patterns:
                    for match in re.finditer(
                        pattern, full_text
                    ):
                        for grp in match.groups():
                            if grp:
                                sec_num = grp.strip().upper()
                                # Only keep sections in valid
                                # IPC range (1-511 + alphanumeric)
                                base_num = re.match(
                                    r'(\d+)', sec_num
                                )
                                if base_num:
                                    n = int(base_num.group(1))
                                    if 1 <= n <= 511:
                                        found_ipc_sections.add(
                                            sec_num
                                        )

                # Also scan for slash-separated sequences
                slash_pattern = (
                    r'(?:[Ss]ec(?:tion)?\.?\s*|[Uu]/[Ss]\.?\s*)'
                    r'(\d+[A-Za-z]*(?:\s*/\s*\d+[A-Za-z]*)+)'
                )
                for match in re.finditer(
                    slash_pattern, full_text
                ):
                    parts = match.group(1).split("/")
                    for part in parts:
                        sec_num = part.strip().upper()
                        base_num = re.match(r'(\d+)', sec_num)
                        if base_num:
                            n = int(base_num.group(1))
                            if 1 <= n <= 511:
                                found_ipc_sections.add(sec_num)

                # Sort by numeric value for display
                def sort_key(s):
                    m = re.match(r'(\d+)(.*)', s)
                    if m:
                        return (int(m.group(1)), m.group(2))
                    return (999, s)

                sorted_ipc = sorted(
                    found_ipc_sections, key=sort_key
                )

                if not sorted_ipc:
                    st.warning(
                        "No IPC section references found in "
                        "this document. The document may already "
                        "use BNS provisions, or the sections may "
                        "be referenced in a format not recognized "
                        "by the scanner."
                    )
                    st.stop()

                st.markdown(
                    '<div class="audit-banner-green">'
                    f'IPC SECTIONS DETECTED — '
                    f'{len(sorted_ipc)} UNIQUE REFERENCE(S) FOUND'
                    '</div>',
                    unsafe_allow_html=True,
                )

            # ── PHASE 3: Automated IPC → BNS Mapping ───────
            with st.spinner(
                "Phase 3/4 — Mapping IPC sections to BNS "
                "equivalents..."
            ):
                all_csv_rows = load_bns_csv_rows()

                transition_table = []
                unmapped_sections = []

                for ipc_sec in sorted_ipc:
                    bns_num = IPC_TO_BNS.get(ipc_sec)
                    ipc_name = get_ipc_section_name(ipc_sec)

                    if bns_num:
                        bns_rows = lookup_ipc_to_bns(
                            ipc_sec, all_csv_rows
                        )
                        bns_name = (
                            bns_rows[0]["section_name"]
                            if bns_rows else "N/A"
                        )
                        bns_desc = (
                            bns_rows[0]["description"][:200]
                            if bns_rows else "N/A"
                        )
                        transition_table.append({
                            "ipc_section": ipc_sec,
                            "ipc_name": ipc_name,
                            "bns_section": bns_num,
                            "bns_name": bns_name,
                            "bns_description": bns_desc,
                            "status": "MAPPED",
                        })
                    else:
                        unmapped_sections.append(ipc_sec)
                        transition_table.append({
                            "ipc_section": ipc_sec,
                            "ipc_name": ipc_name,
                            "bns_section": "—",
                            "bns_name": "Not in mapping",
                            "bns_description": "",
                            "status": "UNMAPPED",
                        })

                mapped_count = len(
                    [t for t in transition_table
                     if t["status"] == "MAPPED"]
                )

                st.markdown(
                    '<div class="audit-banner-green">'
                    f'MAPPING COMPLETE — {mapped_count}/'
                    f'{len(sorted_ipc)} SECTIONS MAPPED TO BNS'
                    '</div>',
                    unsafe_allow_html=True,
                )

                # Display the transition table
                st.markdown(
                    '<div class="section-header" '
                    'style="font-size:1.1rem; margin-top:1rem;">'
                    'IPC → BNS Transition Table</div>',
                    unsafe_allow_html=True,
                )

                table_html = (
                    '<table style="width:100%; '
                    'border-collapse:collapse; '
                    'font-size:0.88rem; '
                    'margin-bottom:1.2rem;">'
                    '<thead>'
                    '<tr style="background-color:#D4AF37; '
                    'color:#1B2A4A;">'
                    '<th style="padding:10px; border:1px solid '
                    '#B8960C; text-align:center; font-weight:800; font-size:0.92rem;">IPC Section</th>'
                    '<th style="padding:10px; border:1px solid '
                    '#B8960C; text-align:left; font-weight:800; font-size:0.92rem;">IPC Offence</th>'
                    '<th style="padding:10px; border:1px solid '
                    '#B8960C; text-align:center; font-weight:800; font-size:0.92rem;">BNS Section</th>'
                    '<th style="padding:10px; border:1px solid '
                    '#B8960C; text-align:left; font-weight:800; font-size:0.92rem;">BNS Provision</th>'
                    '<th style="padding:10px; border:1px solid '
                    '#B8960C; text-align:center; font-weight:800; font-size:0.92rem;">Status</th>'
                    '</tr></thead><tbody>'
                )

                for row in transition_table:
                    status_color = (
                        "#28a745" if row["status"] == "MAPPED"
                        else "#dc3545"
                    )
                    status_badge = (
                        f'<span style="color:{status_color}; '
                        f'font-weight:700;">'
                        f'{row["status"]}</span>'
                    )
                    table_html += (
                        f'<tr style="background-color:#FAFAFA;">'
                        f'<td style="padding:6px; border:1px '
                        f'solid #ccc; text-align:center; '
                        f'font-weight:700;">'
                        f'{row["ipc_section"]}</td>'
                        f'<td style="padding:6px; border:1px '
                        f'solid #ccc;">{row["ipc_name"]}</td>'
                        f'<td style="padding:6px; border:1px '
                        f'solid #ccc; text-align:center; '
                        f'font-weight:700;">'
                        f'{row["bns_section"]}</td>'
                        f'<td style="padding:6px; border:1px '
                        f'solid #ccc;">{row["bns_name"]}</td>'
                        f'<td style="padding:6px; border:1px '
                        f'solid #ccc; text-align:center;">'
                        f'{status_badge}</td>'
                        f'</tr>'
                    )

                table_html += '</tbody></table>'
                st.markdown(table_html, unsafe_allow_html=True)

                if unmapped_sections:
                    st.info(
                        f"⚠ {len(unmapped_sections)} section(s) "
                        f"not found in mapping dictionary: "
                        f"{', '.join(unmapped_sections)}. "
                        f"These may be procedural sections or "
                        f"less common provisions."
                    )

            # ── PHASE 4: AI Batch Interpretation ────────────
            with st.spinner(
                "Phase 4/4 — Generating AI transition "
                "analysis (Llama-3 offline)..."
            ):
                # Build structured context for the LLM
                transition_context = ""
                for i, row in enumerate(transition_table, 1):
                    if row["status"] == "MAPPED":
                        transition_context += (
                            f"{i}. IPC Section "
                            f"{row['ipc_section']} "
                            f"({row['ipc_name']}) → "
                            f"BNS Section "
                            f"{row['bns_section']} "
                            f"({row['bns_name']})\n"
                            f"   BNS Description: "
                            f"{row['bns_description']}\n\n"
                        )

                # Extract a text snippet (first 800 chars)
                doc_snippet = full_text[:800].replace(
                    "\n", " "
                )

                bulk_prompt = (
                    "You are a Senior Legal Clerk in the "
                    "Indian Judicial System specializing in "
                    "the 2023 criminal law reforms.\n\n"
                    "STRICT RULES:\n"
                    "- You are FORBIDDEN from outputting "
                    "internal training tags, mapping codes "
                    "(e.g., map:ipc_bns), version numbers "
                    "(e.g., v1.0), or any metadata.\n"
                    "- Do NOT repeat yourself. State each "
                    "point ONCE.\n"
                    "- Use professional legal formatting.\n"
                    "- No emojis. No hedging. No internal "
                    "codes or tags.\n\n"
                    "DOCUMENT CONTEXT (first 800 chars):\n"
                    f'"""{doc_snippet}"""\n\n'
                    f"The following {mapped_count} IPC sections "
                    f"were identified in this legal document "
                    f"and mapped to their BNS equivalents:\n\n"
                    f"{transition_context}\n"
                    "YOUR TASK:\n"
                    "Summarize how the laws cited in this "
                    "specific document have changed under the "
                    "Bharatiya Nyaya Sanhita 2023. Structure "
                    "your response as follows:\n\n"
                    "DOCUMENT OVERVIEW:\n"
                    "Briefly describe what type of legal "
                    "document this appears to be.\n\n"
                    "TRANSITION SUMMARY TABLE:\n"
                    "For each IPC→BNS mapping found, state:\n"
                    "- Old: IPC Section [N] ([Name])\n"
                    "- New: BNS Section [N] ([Name])\n"
                    "- Change: [Key difference in 1 line]\n\n"
                    "KEY LEGAL IMPLICATIONS:\n"
                    "What are the most important changes for "
                    "practitioners handling this case?\n\n"
                    "PRACTITIONER ACTION ITEMS:\n"
                    "List 3-5 concrete steps a lawyer should "
                    "take to update this document under BNS.\n\n"
                    "Keep the entire response under 500 words. "
                    "Be precise and authoritative."
                )

                bulk_llm = Ollama(
                    model="llama3",
                    temperature=0,
                    num_predict=2048,
                    repeat_penalty=1.3,
                )
                bulk_ai_text = bulk_llm.invoke(
                    bulk_prompt
                ).strip()

                # Safety net: strip leaked tags
                bulk_ai_text = clean_ai_output(bulk_ai_text)

                if not bulk_ai_text:
                    bulk_ai_text = (
                        "The AI model could not generate an "
                        "analysis. Please try again."
                    )

                logger.info("Bulk analysis completed: %d IPC sections mapped.", mapped_count)

            # ── Display AI Analysis ─────────────────────────
            st.markdown(
                '<div class="section-header" '
                'style="font-size:1.1rem; margin-top:1.5rem;">'
                'AI Transition Analysis (Llama-3 — Offline)'
                '</div>',
                unsafe_allow_html=True,
            )

            safe_bulk_ai = html_escape(bulk_ai_text).replace("\n", "<br>")
            st.markdown(
                f'<div class="result-card" '
                f'style="background-color:#F8F9FA; '
                f'padding:1.2rem; border-left:4px solid '
                f'#D4AF37; font-size:0.92rem; '
                f'line-height:1.6; color:#2C3E50;">'
                f'{safe_bulk_ai}</div>',
                unsafe_allow_html=True,
            )

            # ── Document Statistics ─────────────────────────
            st.markdown(
                '<div class="section-header" '
                'style="font-size:1.1rem; margin-top:1.5rem;">'
                'Scan Statistics</div>',
                unsafe_allow_html=True,
            )

            stat_cols = st.columns(4)
            with stat_cols[0]:
                st.metric(
                    "Pages Scanned", total_pages
                )
            with stat_cols[1]:
                st.metric(
                    "IPC Sections Found", len(sorted_ipc)
                )
            with stat_cols[2]:
                st.metric(
                    "Successfully Mapped", mapped_count
                )
            with stat_cols[3]:
                st.metric(
                    "Unmapped",
                    len(unmapped_sections),
                )

            # ── Extracted Text Preview (collapsible) ────────
            with st.expander(
                "View Extracted Document Text", expanded=False
            ):
                for pg in extracted_pages:
                    st.markdown(
                        f'<div style="background:#F0F0F0; '
                        f'padding:0.8rem; margin:0.4rem 0; '
                        f'border-radius:4px; font-size:0.85rem; '
                        f'color:#333;">'
                        f'<strong>Page {pg["page"]}</strong>'
                        f'<hr style="margin:4px 0;">'
                        f'{pg["text"][:1000]}</div>',
                        unsafe_allow_html=True,
                    )
