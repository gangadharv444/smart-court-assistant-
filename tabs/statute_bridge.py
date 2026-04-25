# ============================================================
# Vidhi-AI | Tab 4: IPC-to-BNS Statute Bridge
# ============================================================

import re
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from loaders import load_embeddings, load_bns_vectorstore, load_bns_csv_rows
from ipc_bns_mapping import (
    IPC_TO_BNS, lookup_ipc_to_bns, get_ipc_section_name, contextual_rerank,
)
from utils import clean_ai_output, html_escape
from vidhi_logger import logger

# Import Ollama
try:
    from langchain_community.llms import Ollama
except ImportError:
    from langchain_ollama import OllamaLLM as Ollama


def render():
    """Render the BNS-IPC Statute Bridge tab."""
    st.markdown(
        '<div class="section-header">BNS-IPC Statute Bridge</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="info-label">Search by <strong>IPC section number'
        '</strong> (e.g., IPC 420, IPC 302, 299), '
        '<strong>BNS section number</strong> (e.g., BNS 318, '
        'BNS 103), or <strong>crime name</strong> (e.g., murder, '
        'theft, cheating). The system automatically detects '
        'whether you entered an IPC or BNS number and finds the '
        'correct cross-reference using AI-powered semantic '
        'search across 358 BNS provisions.</p>',
        unsafe_allow_html=True,
    )

    statute_query = st.text_input(
        "Search (IPC number, BNS number, or crime name):",
        value="",
        help="Examples: 'IPC 420', 'IPC 302', '299', 'BNS 103', "
             "'murder', 'theft', 'attempt to murder', "
             "'cheating', 'kidnapping', 'dowry death'",
        key="statute_query",
    )

    run_legal = st.button(
        "Legal Analysis",
        use_container_width=True,
        key="btn_legal_analysis",
    )

    if run_legal:
        if not statute_query.strip():
            st.warning(
                "Please enter a BNS section number or crime description."
            )
        else:
            with st.spinner(
                "Searching BNS database..."
            ):
                query_raw = statute_query.strip()

                # --- IPC-Aware Hybrid Retrieval Logic ---
                query_upper = query_raw.upper().strip()

                # Detect explicit prefix: "IPC 420", "BNS 103"
                has_ipc_prefix = bool(
                    re.match(r'^IPC\s*', query_upper)
                )
                has_bns_prefix = bool(
                    re.match(r'^BNS\s*', query_upper)
                )

                # Extract raw number from input
                num_match = re.search(
                    r'\d+[A-Za-z]*', query_raw
                )
                extracted_number = (
                    num_match.group(0).upper()
                    if num_match else None
                )

                # Determine if query is primarily numeric
                cleaned = (
                    query_upper
                    .replace("BNS", "")
                    .replace("IPC", "")
                    .replace("SECTION", "")
                    .strip()
                )
                # Strip sub-section markers like (1), (2), (a)
                cleaned = re.sub(
                    r'\([^)]*\)', '', cleaned
                ).strip()
                is_numeric_query = (
                    extracted_number is not None
                    and cleaned.replace(" ", "")
                    == extracted_number
                )

                matched_rows = []
                ipc_mode = False  # Track if this is an IPC lookup

                if is_numeric_query and extracted_number:

                    if has_ipc_prefix:
                        # ── PATH A1: Explicit IPC number ─────────
                        ipc_mode = True
                        all_rows = load_bns_csv_rows()
                        ipc_key = extracted_number.upper()
                        dict_rows = lookup_ipc_to_bns(
                            ipc_key, all_rows
                        )
                        if dict_rows:
                            matched_rows = dict_rows[:5]
                        else:
                            # Fallback: semantic search
                            embeddings = load_embeddings()
                            bns_vs = load_bns_vectorstore(
                                embeddings
                            )
                            ipc_query = (
                                f"IPC Section "
                                f"{extracted_number} "
                                f"Indian Penal Code "
                                f"equivalent in "
                                f"Bharatiya Nyaya Sanhita"
                            )
                            sem_results = (
                                bns_vs
                                .similarity_search_with_score(
                                    ipc_query, k=5
                                )
                            )
                            for doc, score in sem_results:
                                if score <= 1.8:
                                    matched_rows.append({
                                        "section":
                                            doc.metadata.get(
                                                "section",
                                                "N/A",
                                            ),
                                        "section_name":
                                            doc.metadata.get(
                                                "section_name",
                                                "N/A",
                                            ),
                                        "description":
                                            doc.metadata.get(
                                                "description",
                                                "",
                                            ),
                                        "chapter":
                                            doc.metadata.get(
                                                "chapter", ""
                                            ),
                                        "chapter_name":
                                            doc.metadata.get(
                                                "chapter_name",
                                                "",
                                            ),
                                        "_score": score,
                                    })

                    elif has_bns_prefix:
                        # ── PATH A2: Explicit BNS number ────────
                        all_rows = load_bns_csv_rows()
                        for row in all_rows:
                            if row["section"] == extracted_number:
                                matched_rows.append(row)
                        if not matched_rows:
                            for row in all_rows:
                                if row["section"].startswith(
                                    extracted_number
                                ):
                                    matched_rows.append(row)
                        matched_rows = matched_rows[:5]

                    else:
                        # ── PATH A3: Bare number (e.g. "420") ───
                        ipc_mode = True

                        all_rows = load_bns_csv_rows()
                        ipc_key = extracted_number.upper()

                        # 1) Deterministic IPC→BNS dictionary
                        dict_rows = lookup_ipc_to_bns(
                            ipc_key, all_rows
                        )

                        # 2) BNS literal lookup
                        bns_literal = []
                        for row in all_rows:
                            if row["section"] == extracted_number:
                                bns_literal.append(row)
                        if not bns_literal:
                            for row in all_rows:
                                if row["section"].startswith(
                                    extracted_number
                                ):
                                    bns_literal.append(row)

                        # 3) Merge: IPC dict results first
                        seen_sections = set()
                        for row in dict_rows + bns_literal:
                            sec = row["section"]
                            if sec not in seen_sections:
                                seen_sections.add(sec)
                                matched_rows.append(row)

                        # 4) If nothing found, fall back to
                        #    semantic search
                        if not matched_rows:
                            embeddings = load_embeddings()
                            bns_vs = load_bns_vectorstore(
                                embeddings
                            )
                            ipc_query = (
                                f"IPC Section "
                                f"{extracted_number} "
                                f"Indian Penal Code "
                                f"equivalent in "
                                f"Bharatiya Nyaya Sanhita"
                            )
                            sem_results = (
                                bns_vs
                                .similarity_search_with_score(
                                    ipc_query, k=5
                                )
                            )
                            for doc, score in sem_results:
                                if score <= 1.8:
                                    matched_rows.append({
                                        "section":
                                            doc.metadata.get(
                                                "section",
                                                "N/A",
                                            ),
                                        "section_name":
                                            doc.metadata.get(
                                                "section_name",
                                                "N/A",
                                            ),
                                        "description":
                                            doc.metadata.get(
                                                "description",
                                                "",
                                            ),
                                        "chapter":
                                            doc.metadata.get(
                                                "chapter", ""
                                            ),
                                        "chapter_name":
                                            doc.metadata.get(
                                                "chapter_name",
                                                "",
                                            ),
                                        "_score": score,
                                    })

                        matched_rows = matched_rows[:5]

                if not matched_rows:
                    # --- PATH B: Text query → semantic search ---
                    embeddings = load_embeddings()
                    bns_vs = load_bns_vectorstore(embeddings)

                    sem_results = (
                        bns_vs.similarity_search_with_score(
                            query_raw, k=5
                        )
                    )

                    for doc, score in sem_results:
                        if score <= 1.8:
                            matched_rows.append({
                                "section": doc.metadata.get(
                                    "section", "N/A"
                                ),
                                "section_name":
                                    doc.metadata.get(
                                        "section_name", "N/A"
                                    ),
                                "description":
                                    doc.metadata.get(
                                        "description", ""
                                    ),
                                "chapter":
                                    doc.metadata.get(
                                        "chapter", ""
                                    ),
                                "chapter_name":
                                    doc.metadata.get(
                                        "chapter_name", ""
                                    ),
                                "_score": score,
                            })

                    # Contextual Re-Ranking for text queries
                    matched_rows = contextual_rerank(
                        query_raw, matched_rows
                    )

            if not matched_rows:
                # No relevant match found -- safety guardrail
                st.markdown(
                    '<div class="audit-banner-red">'
                    'No Matching Section Found</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div class="result-card" '
                    'style="border-left-color:#B71C1C;">'
                    '<strong>This section or crime is not found in the '
                    'verified BNS data.</strong><br><br>'
                    'The search query did not match any provision in '
                    'the Bharatiya Nyaya Sanhita (2023) dataset. '
                    'Please verify the section number or try a '
                    'different crime description.<br><br>'
                    '<em>The AI will not generate an interpretation '
                    'without verified source data to prevent '
                    'hallucinations.</em></div>',
                    unsafe_allow_html=True,
                )
            else:
                # Limit to top 5 candidates
                matched_rows = matched_rows[:5]

                # ── STEP 1: AI-JUDGE SELECTION ───────────────────
                if len(matched_rows) > 1:
                    with st.spinner(
                        "AI Judge is selecting the primary law..."
                    ):
                        # Build compact candidate list
                        candidates = ""
                        for i, row in enumerate(matched_rows, 1):
                            candidates += (
                                f"{i}. Section {row['section']}"
                                f" - {row['section_name']}\n"
                            )

                        # Build IPC-aware selection prompt
                        ipc_hint = ""
                        if ipc_mode and extracted_number:
                            ipc_hint = (
                                f"\nIMPORTANT: The user likely "
                                f"entered OLD IPC Section "
                                f"{extracted_number}. You must "
                                f"select the BNS section that "
                                f"is the NEW equivalent of IPC "
                                f"{extracted_number}, NOT the "
                                f"BNS section that happens to "
                                f"share the same number.\n"
                            )

                        selection_prompt = (
                            "You are a Supreme Court Justice "
                            "of India. A user searched for a "
                            "specific law. Below are candidate "
                            "BNS (Bharatiya Nyaya Sanhita) "
                            "sections retrieved from the "
                            "legal database.\n\n"
                            f"USER QUERY: '{query_raw}'\n"
                            f"{ipc_hint}\n"
                            f"CANDIDATES:\n{candidates}\n"
                            "TASK: Identify the ONE section "
                            "that is the PRIMARY legal match "
                            "for the user's query.\n\n"
                            "SELECTION RULES:\n"
                            "- If the user entered an IPC "
                            "number, pick the BNS section "
                            "that REPLACES that IPC section "
                            "(e.g., IPC 299 → BNS 101, "
                            "IPC 302 → BNS 103, IPC 420 → "
                            "BNS 318). Do NOT pick BNS "
                            "sections that merely share the "
                            "same number.\n"
                            "- 'Attempt to murder' (Section "
                            "109) MUST be prioritized over "
                            "'Attempt to commit culpable "
                            "homicide' (Section 110).\n"
                            "- Always prefer the section "
                            "whose title explicitly matches "
                            "the crime the user intended.\n\n"
                            "RESPOND WITH ONLY THE SECTION "
                            "NUMBER (e.g., 101). Nothing "
                            "else."
                        )

                        judge_llm = Ollama(
                            model="llama3",
                            temperature=0,
                            num_predict=10,
                        )
                        sel_text = judge_llm.invoke(
                            selection_prompt
                        ).strip()

                        # Extract the section number chosen
                        sel_match = re.search(
                            r'(\d+[A-Za-z]*)', sel_text
                        )
                        if sel_match:
                            chosen_section = sel_match.group(1)

                            # Re-order so chosen is first
                            chosen_idx = None
                            for idx, row in enumerate(
                                matched_rows
                            ):
                                if (
                                    row["section"]
                                    == chosen_section
                                ):
                                    chosen_idx = idx
                                    break

                            if (
                                chosen_idx is not None
                                and chosen_idx != 0
                            ):
                                picked = matched_rows.pop(
                                    chosen_idx
                                )
                                matched_rows.insert(0, picked)

                # Now the best match is AI-verified
                best = matched_rows[0]
                section_num = best["section"]
                section_name = best["section_name"]
                chapter = best["chapter"]
                chapter_name = best["chapter_name"]
                description = best["description"]

                # Status banner
                if ipc_mode and extracted_number:
                    ipc_name = get_ipc_section_name(
                        extracted_number.upper()
                    )
                    bns_eq = IPC_TO_BNS.get(
                        extracted_number.upper(), "?"
                    )
                    mode_label = (
                        f"IPC {extracted_number} "
                        f"({ipc_name}) → "
                        f"BNS Section {bns_eq}"
                    )
                else:
                    mode_label = "BNS Provision Match"
                st.markdown(
                    '<div class="audit-banner-green">'
                    f'{mode_label} — '
                    f'{len(matched_rows)} RESULT(S) ANALYZED'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                logger.info("Statute bridge query: %s → BNS %s", query_raw, section_num)

                # Two-column display
                col_law, col_ai = st.columns(2)

                # LEFT COLUMN -- Retrieved Law (AI-selected winner)
                with col_law:
                    st.markdown(
                        '<div class="lang-column-header">'
                        'RETRIEVED LAW</div>',
                        unsafe_allow_html=True,
                    )

                    safe_desc = html_escape(description)
                    st.markdown(
                        f'<div class="lang-text-box">'
                        f'<strong>BNS Section {section_num}'
                        f'</strong><br><br>'
                        f'<strong>Title:</strong> {section_name}'
                        f'<br><br>'
                        f'<strong>Chapter {chapter}:</strong> '
                        f'{chapter_name}<br><br>'
                        f'<strong>Full Description:</strong><br>'
                        f'{safe_desc}</div>',
                        unsafe_allow_html=True,
                    )

                    # Other sections in the "Related" list
                    if len(matched_rows) > 1:
                        st.markdown(
                            '<div class="section-header" '
                            'style="margin-top:1rem; '
                            'font-size:1rem;">'
                            'Other Related Sections</div>',
                            unsafe_allow_html=True,
                        )
                        for extra in matched_rows[1:]:
                            extra_desc = html_escape(
                                extra["description"][:200]
                            )
                            st.markdown(
                                f'<div class="result-card">'
                                f'<strong>BNS Section '
                                f'{extra["section"]}</strong>: '
                                f'{extra["section_name"]}<br>'
                                f'<em>{extra_desc}...</em></div>',
                                unsafe_allow_html=True,
                            )

                # RIGHT COLUMN -- AI Interpretation
                with col_ai:
                    st.markdown(
                        '<div class="lang-column-header">'
                        'AI INTERPRETATION</div>',
                        unsafe_allow_html=True,
                    )

                    with st.spinner(
                        "Generating legal interpretation..."
                    ):
                        # Build context from all matched rows
                        context_block = ""
                        for i, row in enumerate(
                            matched_rows, 1
                        ):
                            context_block += (
                                f"Match {i}: BNS Section "
                                f"{row['section']} - "
                                f"{row['section_name']}\n"
                                f"Description: "
                                f"{row['description'][:500]}"
                                f"\n\n"
                            )

                        # Build IPC-aware interpretation
                        ipc_context = ""
                        if ipc_mode and extracted_number:
                            ipc_context = (
                                f"The user searched for OLD IPC "
                                f"Section {extracted_number}. "
                                f"The AI-Judge identified BNS "
                                f"Section {section_num} as its "
                                f"replacement under the 2023 "
                                f"reforms. Explain this mapping "
                                f"clearly.\n\n"
                            )

                        interpret_prompt = (
                            "You are a Senior Indian Legal "
                            "Expert specializing in the 2023 "
                            "criminal law reforms that replaced "
                            "the Indian Penal Code (IPC) with "
                            "the Bharatiya Nyaya Sanhita "
                            "(BNS).\n\n"
                            "STRICT RULES:\n"
                            "- You are FORBIDDEN from outputting "
                            "internal training tags, mapping "
                            "codes (e.g., map:ipc_bns), version "
                            "numbers (e.g., v1.0), or any "
                            "metadata. NEVER output these.\n"
                            "- Begin directly with a professional "
                            "legal explanation.\n"
                            "- Do NOT repeat yourself. State "
                            "each point ONCE.\n"
                            "- Keep your response concise and "
                            "structured (under 300 words).\n\n"
                            f"USER QUERY: '{query_raw}'\n\n"
                            f"{ipc_context}"
                            f"The AI-Judge has determined that "
                            f"BNS Section {section_num} "
                            f"({section_name}) is the primary "
                            f"match.\n\n"
                            f"ALL RETRIEVED PROVISIONS:\n"
                            f"{context_block}\n"
                            "YOUR RESPONSE (structured):\n\n"
                            "PRIMARY MATCH:\n"
                            f"Explain BNS Section {section_num} "
                            "and what crime it covers.\n\n"
                            "IPC EQUIVALENT:\n"
                            "State: 'This corresponds to Old "
                            "IPC Section [Number] - [Name].'\n\n"
                            "KEY CHANGES:\n"
                            "Note differences between old IPC "
                            "and new BNS provision.\n\n"
                            "PRACTITIONER GUIDANCE:\n"
                            "State practical significance.\n\n"
                            "RELATED SECTIONS:\n"
                            "Briefly list how the other "
                            "retrieved sections relate (one "
                            "line each).\n\n"
                            "No emojis. No hedging. No internal "
                            "codes or tags."
                        )

                        interpret_llm = Ollama(
                            model="llama3",
                            temperature=0,
                            num_predict=1024,
                            repeat_penalty=1.3,
                        )
                        ai_text = interpret_llm.invoke(
                            interpret_prompt
                        ).strip()

                        # Safety net: strip any leaked tags
                        ai_text = clean_ai_output(ai_text)

                        if not ai_text:
                            ai_text = (
                                "The AI model did not produce "
                                "an interpretation for this "
                                "section. This may occur for "
                                "very short or preliminary "
                                "sections."
                            )

                    safe_ai = html_escape(ai_text).replace("\n", "<br>")
                    st.markdown(
                        f'<div class="lang-text-box">'
                        f'{safe_ai}</div>',
                        unsafe_allow_html=True,
                    )
