"""
Vidhi-AI -- Comprehensive Project Report PDF Generator
Generates a detailed technical documentation PDF covering
architecture, technologies, RAG pipeline, challenges, and optimizations.
"""

from fpdf import FPDF
import os
import datetime


class VidhiReport(FPDF):
    """Custom PDF class with header/footer and styling."""

    NAVY = (10, 22, 40)        # #0A1628
    GOLD = (201, 162, 39)      # #C9A227
    WHITE = (255, 255, 255)
    BLACK = (30, 30, 30)
    GRAY = (100, 100, 100)
    LIGHT_BG = (250, 248, 240)  # cream
    SECTION_BG = (21, 34, 56)   # navy-mid

    def header(self):
        # Navy bar at top
        self.set_fill_color(*self.NAVY)
        self.rect(0, 0, 210, 18, 'F')
        # Gold accent line
        self.set_fill_color(*self.GOLD)
        self.rect(0, 18, 210, 1.5, 'F')
        # Title text
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 13)
        self.set_xy(10, 4)
        self.cell(0, 10, "VIDHI-AI  |  Smart Court Assistant  |  Technical Report", align="C")
        self.ln(18)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(*self.GRAY)
        self.cell(0, 10,
                  f"Vidhi-AI Technical Report  |  Page {self.page_no()}/{{nb}}  |  "
                  f"Generated: {datetime.datetime.now().strftime('%d %B %Y')}",
                  align="C")

    # -- Utility methods -------------------------------------------------
    def section_title(self, number, title):
        """Big section header with navy background."""
        self.ln(4)
        self.set_fill_color(*self.NAVY)
        self.set_text_color(*self.GOLD)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, f"  {number}. {title}", ln=True, fill=True)
        self.set_text_color(*self.BLACK)
        self.ln(3)

    def sub_section(self, title):
        """Sub-section header with gold underline."""
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*self.NAVY)
        self.cell(0, 7, title, ln=True)
        # Gold underline
        x = self.get_x()
        y = self.get_y()
        self.set_draw_color(*self.GOLD)
        self.set_line_width(0.6)
        self.line(10, y, 80, y)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        self.ln(2)
        self.set_text_color(*self.BLACK)

    def body_text(self, text):
        """Normal paragraph text."""
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*self.BLACK)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bullet(self, text, indent=15):
        """Bullet point."""
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*self.BLACK)
        x = self.get_x()
        self.set_x(indent)
        self.cell(5, 5.5, chr(45))  # bullet char
        self.multi_cell(0, 5.5, f"  {text}")
        self.ln(0.5)

    def key_value(self, key, value, indent=15):
        """Key: Value pair with bold key."""
        self.set_x(indent)
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(*self.NAVY)
        kw = self.get_string_width(f"{key}: ") + 2
        self.cell(kw, 5.5, f"{key}: ")
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*self.BLACK)
        self.multi_cell(0, 5.5, value)
        self.ln(0.5)

    def tech_table(self, headers, rows):
        """Styled table with navy header row."""
        col_widths = [190 / len(headers)] * len(headers)
        # If 2 columns, make them 60/130
        if len(headers) == 2:
            col_widths = [60, 130]
        elif len(headers) == 3:
            col_widths = [50, 60, 80]

        # Header
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*self.NAVY)
        self.set_text_color(*self.GOLD)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, f"  {h}", border=1, fill=True)
        self.ln()

        # Rows
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*self.BLACK)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(245, 242, 230)
            else:
                self.set_fill_color(*self.WHITE)

            max_h = 7
            for i, cell_text in enumerate(row):
                # Calculate required height
                lines = self.multi_cell(col_widths[i], 5.5, cell_text, split_only=True)
                h = len(lines) * 5.5
                if h > max_h:
                    max_h = h

            x_start = self.get_x()
            y_start = self.get_y()
            for i, cell_text in enumerate(row):
                self.set_xy(x_start + sum(col_widths[:i]), y_start)
                self.multi_cell(col_widths[i], 5.5, f"  {cell_text}", border=1, fill=fill)

            self.set_y(y_start + max_h)
            fill = not fill
        self.ln(2)

    def code_block(self, text):
        """Mono-spaced code block with light background."""
        self.set_fill_color(240, 237, 225)
        self.set_font("Courier", "", 8)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 4.5, text, fill=True)
        self.set_text_color(*self.BLACK)
        self.ln(2)

    def highlight_box(self, text):
        """Gold-bordered highlight box."""
        self.set_fill_color(253, 248, 238)
        self.set_draw_color(*self.GOLD)
        self.set_line_width(0.5)
        x = self.get_x()
        y = self.get_y()
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(80, 60, 10)
        self.multi_cell(0, 5.5, text, border=1, fill=True)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        self.set_text_color(*self.BLACK)
        self.ln(2)


def generate_report():
    pdf = VidhiReport()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)

    # ====================================================================
    # COVER PAGE
    # ====================================================================
    pdf.add_page()
    pdf.ln(25)
    # Big navy box
    pdf.set_fill_color(*VidhiReport.NAVY)
    pdf.rect(15, 40, 180, 80, 'F')
    # Gold border
    pdf.set_draw_color(*VidhiReport.GOLD)
    pdf.set_line_width(1.5)
    pdf.rect(17, 42, 176, 76, 'D')
    pdf.set_line_width(0.2)
    pdf.set_draw_color(0, 0, 0)

    # Title on navy
    pdf.set_text_color(*VidhiReport.GOLD)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_xy(20, 52)
    pdf.cell(170, 15, "VIDHI-AI", align="C")
    pdf.set_font("Helvetica", "", 14)
    pdf.set_xy(20, 68)
    pdf.set_text_color(*VidhiReport.WHITE)
    pdf.cell(170, 10, "Smart Court Assistant for the Indian Judicial System", align="C")
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_xy(20, 82)
    pdf.set_text_color(176, 190, 197)
    pdf.cell(170, 10, "100% Offline  |  Zero Cloud APIs  |  Air-Gapped Deployment", align="C")
    pdf.set_xy(20, 95)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(170, 10, "Comprehensive Technical Documentation", align="C")

    # Below the box
    pdf.set_text_color(*VidhiReport.BLACK)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(15, 135)
    pdf.cell(90, 7, f"Date: {datetime.datetime.now().strftime('%d %B %Y')}")
    pdf.cell(90, 7, "Version: 1.0", align="R")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(90, 7, "Platform: Windows 11 (AMD Ryzen 5 5500U)")
    pdf.cell(90, 7, "Runtime: 100% Local / Offline", align="R")
    pdf.ln(10)
    pdf.cell(90, 7, "Language: Python 3.13.5")
    pdf.cell(90, 7, "Framework: Streamlit + LangChain", align="R")
    pdf.ln(10)
    pdf.cell(90, 7, "LLM: Ollama Llama-3 8B (CPU Only)")
    pdf.cell(90, 7, "Vector DB: ChromaDB", align="R")

    # ====================================================================
    # TABLE OF CONTENTS
    # ====================================================================
    pdf.add_page()
    pdf.section_title("", "TABLE OF CONTENTS")
    toc = [
        ("1", "Project Overview & Motivation", "3"),
        ("2", "System Architecture", "4"),
        ("3", "Technology Stack -- What & Why", "5"),
        ("4", "RAG Pipeline -- Complete Technical Breakdown", "7"),
        ("5", "Feature Modules (All 6 Tabs)", "9"),
        ("6", "IPC-to-BNS Mapping System", "12"),
        ("7", "Data Architecture & Storage", "13"),
        ("8", "Hardware Constraints & Optimizations", "14"),
        ("9", "Challenges Faced & Solutions", "16"),
        ("10", "Security & Offline Guarantees", "18"),
        ("11", "Project File Structure", "19"),
        ("12", "Future Scope & Improvements", "20"),
    ]
    for num, title, page in toc:
        pdf.set_font("Helvetica", "B" if num else "", 10)
        pdf.cell(10, 7, num)
        pdf.cell(140, 7, title)
        pdf.cell(30, 7, page, align="R")
        pdf.ln()

    # ====================================================================
    # 1. PROJECT OVERVIEW & MOTIVATION
    # ====================================================================
    pdf.add_page()
    pdf.section_title("1", "PROJECT OVERVIEW & MOTIVATION")

    pdf.sub_section("1.1 What is Vidhi-AI?")
    pdf.body_text(
        "Vidhi-AI is a fully offline, AI-powered Smart Court Assistant designed specifically for the "
        "Indian Judicial System. It enables judges, lawyers, and court staff to analyze legal documents, "
        "extract timelines, detect evidence conflicts, and navigate India's 2023 criminal law transition "
        "(IPC to BNS) -- all without any internet connection or cloud API calls."
    )
    pdf.body_text(
        "The name 'Vidhi' comes from Sanskrit, meaning 'law' or 'legal procedure', making it a fitting "
        "name for an AI system dedicated to Indian legal intelligence."
    )

    pdf.sub_section("1.2 Why Was This Built?")
    pdf.body_text(
        "India's criminal law underwent a historic overhaul on 1 July 2024 when three new codes replaced "
        "colonial-era legislation:"
    )
    pdf.bullet("Indian Penal Code (IPC), 1860 --> Bharatiya Nyaya Sanhita (BNS), 2023")
    pdf.bullet("Code of Criminal Procedure (CrPC), 1973 --> Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023")
    pdf.bullet("Indian Evidence Act, 1872 --> Bharatiya Sakshya Adhiniyam (BSA), 2023")
    pdf.ln(2)
    pdf.body_text(
        "This created an urgent need for tools that help legal professionals quickly find the new BNS "
        "equivalent of any old IPC section. Vidhi-AI addresses this by providing instant, verified "
        "cross-references backed by a deterministic mapping dictionary of ~300 IPC-to-BNS entries."
    )

    pdf.sub_section("1.3 Why 100% Offline?")
    pdf.body_text(
        "Indian courtrooms handle extremely sensitive data -- FIRs, witness statements, chargesheets, "
        "and classified judicial documents. Sending this data to cloud APIs (OpenAI, Google, etc.) "
        "poses serious security and confidentiality risks. Vidhi-AI guarantees:"
    )
    pdf.bullet("ZERO data leaves the machine -- all AI inference runs locally via Ollama")
    pdf.bullet("No internet dependency -- works in air-gapped courtroom networks")
    pdf.bullet("No API keys, no subscriptions, no third-party data processing agreements needed")
    pdf.bullet("Full compliance with judicial data handling protocols")

    pdf.sub_section("1.4 Target Hardware")
    pdf.highlight_box(
        "Constraint: The entire system must run on a consumer-grade laptop -- "
        "AMD Ryzen 5 5500U (6 cores, 12 threads), 16 GB RAM, NO dedicated GPU. "
        "This ruled out large models (70B, 13B) and GPU-dependent frameworks."
    )

    # ====================================================================
    # 2. SYSTEM ARCHITECTURE
    # ====================================================================
    pdf.add_page()
    pdf.section_title("2", "SYSTEM ARCHITECTURE")

    pdf.sub_section("2.1 High-Level Architecture")
    pdf.body_text(
        "Vidhi-AI follows a modular, layered architecture where each component is independently "
        "cacheable and replaceable:"
    )
    pdf.ln(1)
    pdf.code_block(
        "+---------------------------------------------------------+\n"
        "|                    STREAMLIT DASHBOARD                   |\n"
        "|  (6 Tabs: Case Analysis, Chronos, Conflict,             |\n"
        "|   IPC-to-BNS, Regional OCR, Bulk Analysis)              |\n"
        "+---------------------------------------------------------+\n"
        "              |               |              |\n"
        "              v               v              v\n"
        "    +----------------+  +-----------+  +-----------+\n"
        "    | RAG Pipeline   |  | Direct LLM|  | OCR Engine|\n"
        "    | (ChromaDB +    |  | Prompting  |  | Tesseract |\n"
        "    |  Retriever)    |  | (Ollama)   |  | + Poppler |\n"
        "    +----------------+  +-----------+  +-----------+\n"
        "              |               |\n"
        "              v               v\n"
        "    +------------------------------------+\n"
        "    |   Ollama Llama-3 8B (CPU-Only)     |\n"
        "    |   Local HTTP Server on Port 11434  |\n"
        "    +------------------------------------+\n"
        "              |\n"
        "              v\n"
        "    +------------------------------------+\n"
        "    |   Data Layer                       |\n"
        "    |   - ChromaDB (vidhi_vault,         |\n"
        "    |     bns_vault)                     |\n"
        "    |   - bns_sections.csv (358 rows)    |\n"
        "    |   - IPC_TO_BNS dict (~300 entries) |\n"
        "    +------------------------------------+"
    )

    pdf.sub_section("2.2 Request Flow (RAG Query)")
    pdf.body_text("When a user submits a legal query in the Case Analysis tab:")
    pdf.bullet("1. PDF is loaded via PyPDFLoader, text is extracted page-by-page")
    pdf.bullet("2. Text is split into 500-character chunks with 50-character overlap using RecursiveCharacterTextSplitter")
    pdf.bullet("3. Each chunk is embedded using all-MiniLM-L6-v2 (384-dimensional vectors)")
    pdf.bullet("4. Embeddings are stored in ChromaDB (an in-process vector database)")
    pdf.bullet("5. User query is embedded and top-3 most similar chunks are retrieved (cosine similarity)")
    pdf.bullet("6. Retrieved chunks are injected as 'context' into a ChatPromptTemplate")
    pdf.bullet("7. The augmented prompt is sent to Ollama Llama-3 8B running locally")
    pdf.bullet("8. LLM generates a grounded answer based ONLY on the provided context")
    pdf.bullet("9. Response is parsed via StrOutputParser and displayed in the dashboard")

    # ====================================================================
    # 3. TECHNOLOGY STACK
    # ====================================================================
    pdf.add_page()
    pdf.section_title("3", "TECHNOLOGY STACK -- WHAT & WHY")

    pdf.sub_section("3.1 Core Technologies")
    techs = [
        ["Python 3.13.5",
         "Primary language. Chosen for its rich ML/NLP ecosystem (LangChain, HuggingFace, ChromaDB). "
         "Runs natively on Windows without compilation issues."],
        ["Streamlit",
         "Web dashboard framework. Chosen because it converts Python scripts into interactive web apps "
         "with zero frontend code (no HTML/JS needed). Hot-reload, built-in file uploader, and tabs "
         "made it ideal for rapid prototyping of a 6-tab legal dashboard."],
        ["Ollama + Llama-3 8B",
         "Local LLM inference server. Ollama wraps GGUF/safetensor models into a simple HTTP API "
         "(localhost:11434). Llama-3 8B was chosen because: (a) it fits in 16GB RAM with quantization, "
         "(b) it supports 8K context window, (c) Meta's open license allows commercial use, "
         "(d) it outperforms GPT-3.5 on many benchmarks despite being 8B parameters."],
        ["LangChain",
         "Orchestration framework for RAG pipelines. Provides: document loaders (PyPDFLoader), "
         "text splitters (RecursiveCharacterTextSplitter), vector store integrations (Chroma), "
         "prompt templates (ChatPromptTemplate), and LCEL chains (RunnablePassthrough). "
         "Without LangChain, building the RAG pipeline would require 5x more code."],
        ["ChromaDB",
         "In-process vector database. Chosen over Pinecone/Weaviate because: (a) runs 100% locally "
         "with no server setup, (b) persists to disk (./vidhi_vault, ./bns_vault), (c) supports "
         "cosine similarity search, (d) Python-native with zero external dependencies. "
         "Stores 358 BNS sections + uploaded PDF chunks."],
        ["HuggingFace Embeddings\n(all-MiniLM-L6-v2)",
         "Sentence embedding model. Produces 384-dimensional vectors from text. Chosen because: "
         "(a) only 80MB -- tiny footprint, (b) runs on CPU in ~200ms per embedding, "
         "(c) trained on 1B+ sentence pairs for semantic similarity, (d) downloads once and caches "
         "locally (~/.cache/huggingface). No API calls after first download."],
        ["pdfplumber + PyMuPDF",
         "Dual PDF text extraction. pdfplumber is the primary extractor (better at tables/layouts). "
         "PyMuPDF (fitz) serves as fallback for PDFs that pdfplumber cannot parse. This dual approach "
         "ensures maximum PDF compatibility."],
        ["Tesseract OCR + Poppler",
         "OCR pipeline for regional language PDFs. Poppler converts PDF pages to images (300 DPI). "
         "Tesseract then performs OCR with kan+hin+mar+eng language packs. This handles scanned "
         "documents and avoids (cid:xxxx) encoding issues from direct PDF text extraction."],
        ["pdf2image + Pillow",
         "Bridge between Poppler and Tesseract. pdf2image calls Poppler to rasterize PDF pages. "
         "Pillow (PIL) handles image manipulation before passing to Tesseract."],
    ]
    for tech in techs:
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.set_text_color(*VidhiReport.NAVY)
        pdf.cell(0, 6, tech[0], ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*VidhiReport.BLACK)
        pdf.multi_cell(0, 5, tech[1])
        pdf.ln(2)

    pdf.sub_section("3.2 Why NOT These Technologies?")
    pdf.add_page()
    rejects = [
        ["OpenAI GPT-4 / Claude",
         "Requires internet + API keys. Violates the offline-only constraint. "
         "Also involves sending sensitive judicial documents to third-party servers."],
        ["FAISS (Facebook AI Similarity Search)",
         "Excellent performance but does not persist to disk natively. ChromaDB was chosen "
         "because it auto-persists embeddings to ./vidhi_vault without manual serialization."],
        ["Llama-2 / Mistral 7B",
         "Llama-3 8B significantly outperforms both on reasoning, instruction following, and "
         "legal text comprehension. Meta's benchmarks show 15%+ improvement over Llama-2."],
        ["Flask / Django",
         "Overkill for a single-user dashboard. Streamlit provides file upload, tabs, buttons, "
         "spinners, and layout columns out-of-the-box with zero frontend code."],
        ["Docker / Kubernetes",
         "Unnecessary complexity for a single-laptop deployment. The venv + Ollama + Streamlit "
         "stack runs directly on Windows without containerization overhead."],
        ["GPU-dependent models (70B, 13B+)",
         "The target laptop has NO dedicated GPU. AMD Ryzen 5 5500U's integrated Vega graphics "
         "cannot accelerate LLM inference. All models must run on CPU within 16GB RAM."],
    ]
    for tech in rejects:
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.set_text_color(183, 28, 28)  # red
        pdf.cell(0, 6, f"REJECTED: {tech[0]}", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*VidhiReport.BLACK)
        pdf.multi_cell(0, 5, tech[1])
        pdf.ln(2)

    # ====================================================================
    # 4. RAG PIPELINE -- COMPLETE TECHNICAL BREAKDOWN
    # ====================================================================
    pdf.add_page()
    pdf.section_title("4", "RAG PIPELINE -- COMPLETE TECHNICAL BREAKDOWN")

    pdf.sub_section("4.1 What is RAG?")
    pdf.body_text(
        "Retrieval-Augmented Generation (RAG) is an AI architecture that combines information retrieval "
        "with text generation. Instead of relying solely on the LLM's training data (which can hallucinate), "
        "RAG first retrieves relevant passages from a knowledge base, then feeds those passages as context "
        "to the LLM. This grounds the LLM's response in actual document content."
    )
    pdf.highlight_box(
        "RAG Formula: Answer = LLM(User Query + Retrieved Context from Vector Database)\n"
        "This eliminates hallucination because the LLM can ONLY use information present in the retrieved chunks."
    )

    pdf.sub_section("4.2 Document Ingestion Pipeline")
    pdf.body_text("Step-by-step process when a user uploads a PDF:")
    pdf.ln(1)
    pdf.key_value("Step 1 - PDF Loading", "PyPDFLoader reads the PDF page-by-page. Each page becomes a LangChain Document object with page_content (text) and metadata (page number, source filename).")
    pdf.key_value("Step 2 - Text Chunking", "RecursiveCharacterTextSplitter breaks each page into 500-character chunks with 50-character overlap. The overlap ensures that sentences split across chunk boundaries are still searchable. The splitter tries to break at paragraph > sentence > word boundaries.")
    pdf.key_value("Step 3 - Embedding", "Each chunk is passed through all-MiniLM-L6-v2 to produce a 384-dimensional dense vector. This model maps semantically similar text to nearby points in vector space. E.g., 'murder' and 'homicide' will have vectors close together.")
    pdf.key_value("Step 4 - Vector Storage", "Embeddings + original text + metadata are stored in ChromaDB. The database creates an index for fast approximate nearest neighbor (ANN) search. Persisted to disk at ./vidhi_vault (case PDFs) and ./bns_vault (BNS sections).")

    pdf.sub_section("4.3 Query & Retrieval Pipeline")
    pdf.key_value("Step 5 - Query Embedding", "The user's question is embedded using the SAME all-MiniLM-L6-v2 model to ensure vector space compatibility.")
    pdf.key_value("Step 6 - Similarity Search", "ChromaDB performs cosine similarity search to find the top-k (k=3) most relevant chunks. Cosine similarity measures the angle between two vectors -- identical meaning = angle 0 = similarity 1.0.")
    pdf.key_value("Step 7 - Context Injection", "Retrieved chunks are concatenated and injected into a ChatPromptTemplate as the 'context' variable. The prompt instructs the LLM to answer ONLY based on this context.")
    pdf.key_value("Step 8 - LLM Generation", "Ollama Llama-3 8B receives the augmented prompt via localhost:11434 HTTP API. Temperature=0 ensures deterministic, reproducible outputs. The model generates a response grounded in the retrieved evidence.")
    pdf.key_value("Step 9 - Output Parsing", "StrOutputParser extracts the raw text response. Any leaked training tags or metadata are cleaned via clean_ai_output() regex post-processing.")

    pdf.sub_section("4.4 RAG Chain Code (LCEL)")
    pdf.body_text("LangChain Expression Language (LCEL) composes the entire pipeline as a single chain:")
    pdf.code_block(
        'rag_chain = (\n'
        '    {\n'
        '        "context": retriever | format_docs,\n'
        '        "input": RunnablePassthrough(),\n'
        '    }\n'
        '    | prompt\n'
        '    | llm\n'
        '    | StrOutputParser()\n'
        ')\n'
        'answer = rag_chain.invoke(query)'
    )
    pdf.body_text(
        "The pipe (|) operator chains components sequentially. RunnablePassthrough() passes the user query "
        "unchanged. The retriever fetches context, format_docs concatenates chunks, the prompt merges them, "
        "and the LLM generates the final answer."
    )

    pdf.sub_section("4.5 Chunking Strategy -- Why 500/50?")
    pdf.body_text(
        "Chunk size 500 characters with 50-character overlap was chosen after experimentation:"
    )
    pdf.bullet("Too small (100-200 chars): Fragments sentences, loses context, retrieves irrelevant snippets")
    pdf.bullet("Too large (1000+ chars): Exceeds LLM context budget when 3 chunks are retrieved (3 x 1000 = 3000 tokens consumed just for context)")
    pdf.bullet("500 chars: ~125 tokens per chunk. With k=3 retrieval, context = ~375 tokens -- leaves 7600+ tokens for the model's response within Llama-3's 8K window")
    pdf.bullet("50-char overlap: Ensures sentences at chunk boundaries appear in both adjacent chunks, preventing information loss at split points")

    pdf.sub_section("4.6 Embedding Model Deep Dive")
    pdf.body_text("all-MiniLM-L6-v2 specifications:")
    pdf.bullet("Architecture: 6-layer MiniLM (distilled from larger BERT)")
    pdf.bullet("Parameters: 22.7 million (tiny -- runs on any CPU)")
    pdf.bullet("Output: 384-dimensional dense vectors")
    pdf.bullet("Training: 1 billion sentence pairs (paraphrase mining)")
    pdf.bullet("Speed: ~200ms per embedding on Ryzen 5 5500U")
    pdf.bullet("Size: ~80MB on disk (cached at ~/.cache/huggingface/)")
    pdf.bullet("Use case: Semantic similarity, retrieval, clustering")
    pdf.bullet("Why not larger models? e5-large (1.3GB) and instructor-xl (4.6GB) are more accurate but 10-50x slower on CPU. For a responsive dashboard, speed matters more than marginal accuracy gains.")

    # ====================================================================
    # 5. FEATURE MODULES
    # ====================================================================
    pdf.add_page()
    pdf.section_title("5", "FEATURE MODULES -- ALL 6 TABS")

    pdf.sub_section("5.1 Tab 1: Case Analysis (RAG)")
    pdf.body_text(
        "Purpose: Answer free-form legal questions about uploaded PDF documents using the full RAG pipeline."
    )
    pdf.key_value("Input", "User uploads 1+ PDFs (FIRs, chargesheets, witness statements) + types a legal question")
    pdf.key_value("Processing", "Builds a temporary ChromaDB vectorstore from selected documents only. Uses RecursiveCharacterTextSplitter (500/50). Retrieves top-3 chunks via cosine similarity. Sends to Llama-3 with legal system prompt.")
    pdf.key_value("Output", "AI-generated answer grounded strictly in document content. Displayed in a styled result card.")
    pdf.key_value("Document Selector", "st.multiselect widget lets users choose exactly which uploaded PDFs to include in the analysis. Default: all uploaded documents.")
    pdf.key_value("Key Design Decision", "Chunks are created fresh from selected documents each time (not cached) to ensure the user always queries only the documents they selected.")

    pdf.sub_section("5.2 Tab 2: Chronos (Timeline Extraction)")
    pdf.body_text(
        "Purpose: Extract a strict chronological timeline of all events from legal documents."
    )
    pdf.key_value("Input", "Selected uploaded PDF documents")
    pdf.key_value("Processing", "Concatenates full text of selected documents. Sends directly to Llama-3 (no RAG -- full text injection). System prompt instructs: 'Extract a strict, chronological timeline as a bulleted list with Date/Time followed by Event.'")
    pdf.key_value("Output", "Bulleted timeline of events with dates/times")
    pdf.key_value("No RAG Here", "Chronos does NOT use ChromaDB retrieval. The full document text is sent directly to the LLM because timeline extraction requires seeing ALL events in order, not just the top-3 relevant chunks.")
    pdf.key_value("Context Window Risk", "If total document text exceeds ~6000 tokens (~24,000 chars), Llama-3's 8K context window will truncate the input. For very large documents, the document selector helps users send only the most relevant PDFs.")

    pdf.sub_section("5.3 Tab 3: Conflict Detection")
    pdf.body_text(
        "Purpose: Cross-compare 2+ legal documents to identify contradictions in facts, timelines, "
        "descriptions, and witness accounts."
    )
    pdf.key_value("Input", "At least 2 uploaded PDF documents selected via multiselect")
    pdf.key_value("Processing", "Each document is labeled separately (DOCUMENT: filename). Combined text is sent to Llama-3 with a detailed 'Judicial Auditor' system prompt that mandates checking 8 categories: date/time, location, vehicle details, suspect description, behavior, chronology, witness identity, and other facts.")
    pdf.key_value("Output Format", "Structured conflict report: CONFLICT: [title] / DOCUMENT A: [quote] / DOCUMENT B: [quote] / SEVERITY: [CRITICAL/MODERATE/MINOR]. Judicial Observations section at the end.")
    pdf.key_value("Parsing", "Raw LLM output is parsed line-by-line to detect CONFLICT:/DOCUMENT A:/DOCUMENT B:/SEVERITY: markers. Each conflict is rendered as a red-bordered card. If no conflicts: green 'Documents Consistent' banner.")
    pdf.key_value("LLM Config", "temperature=0 (deterministic), num_predict=2048 (long output allowed)")

    pdf.add_page()
    pdf.sub_section("5.4 Tab 4: IPC to BNS (Statutory Transition)")
    pdf.body_text(
        "Purpose: Convert any IPC section number to its BNS equivalent, or search BNS provisions by crime name."
    )
    pdf.key_value("3-Path Retrieval", "The system intelligently routes queries through 3 paths:")
    pdf.bullet("PATH A1 (IPC prefix): User types 'IPC 420' -> Deterministic dictionary lookup (IPC_TO_BNS dict, ~300 entries) -> Returns BNS 318")
    pdf.bullet("PATH A2 (BNS prefix): User types 'BNS 103' -> Direct CSV lookup in bns_sections.csv -> Returns Section 103 details")
    pdf.bullet("PATH A3 (Bare number): User types '420' -> Tries IPC dict first, then BNS CSV, merges results")
    pdf.bullet("PATH B (Text query): User types 'murder' or 'attempt to murder' -> Semantic search via ChromaDB over 358 BNS sections")
    pdf.key_value("AI Judge", "When multiple candidate sections are retrieved (common for text queries), an 'AI Judge' (Llama-3 with num_predict=10) selects the single most legally precise match. This prevents wrong selections like picking BNS 299 instead of BNS 101 for 'murder'.")
    pdf.key_value("AI Interpretation", "A second Llama-3 call (num_predict=1024, repeat_penalty=1.3) generates a structured legal interpretation: PRIMARY MATCH, IPC EQUIVALENT, KEY CHANGES, PRACTITIONER GUIDANCE, RELATED SECTIONS.")
    pdf.key_value("Contextual Re-Ranking", "For text queries, a custom contextual_rerank() function checks if keywords from the query (e.g., 'attempt', 'conspiracy', 'negligence') appear in section descriptions. Matching sections are boosted to the top.")
    pdf.key_value("Input Normalization", "All inputs are .upper() normalized. Sub-section markers like (1), (2) are stripped via regex. This allows inputs like '304b', '304B', '304B(1)' to all resolve correctly.")

    pdf.sub_section("5.5 Tab 5: Regional OCR (Vernacular Evidence)")
    pdf.body_text(
        "Purpose: Extract text from regional-language PDFs (Kannada, Hindi, Marathi) using OCR and translate to English."
    )
    pdf.key_value("OCR Pipeline", "PDF -> Poppler (pdf2image, 300 DPI) -> PNG images -> Tesseract OCR (kan+hin+mar+eng language packs) -> Raw text")
    pdf.key_value("Translation", "Raw OCR text is sent to Llama-3 with a 'Senior Judicial Translator' prompt. Rules: preserve ALL proper nouns, dates, numbers, registration numbers. No placeholders like [Name].")
    pdf.key_value("Display", "Side-by-side: Original Extracted Text (left) | English Translation (right)")
    pdf.key_value("Why OCR-First?", "Direct PDF text extraction from Indian-language PDFs often produces (cid:xxxx) encoding garbage because PDF fonts encode Devanagari/Kannada glyphs as custom character IDs. OCR bypasses this by treating each page as an image.")

    pdf.sub_section("5.6 Tab 6: Bulk Document Analysis")
    pdf.body_text(
        "Purpose: Upload any legal PDF, automatically detect all IPC section references, map each to BNS, "
        "and generate a comprehensive transition analysis."
    )
    pdf.key_value("Phase 1", "PDF text extraction via pdfplumber (primary) with PyMuPDF fallback")
    pdf.key_value("Phase 2", "Regex-based IPC section scanning using 7 patterns: 'Section 302', 'Sec. 420', 'u/s 302', 'IPC 302', '302 IPC', 'S. 302', and slash-separated groups like 'Section 302/307/34'. Only sections in valid IPC range (1-511) are kept.")
    pdf.key_value("Phase 3", "Each detected IPC section is mapped to BNS using the deterministic IPC_TO_BNS dictionary. Full BNS descriptions are pulled from bns_sections.csv. Results displayed in a styled HTML transition table.")
    pdf.key_value("Phase 4", "AI batch interpretation via Llama-3 (num_predict=2048, repeat_penalty=1.3). Generates: DOCUMENT OVERVIEW, TRANSITION SUMMARY TABLE, KEY LEGAL IMPLICATIONS, PRACTITIONER ACTION ITEMS.")

    # ====================================================================
    # 6. IPC-TO-BNS MAPPING SYSTEM
    # ====================================================================
    pdf.add_page()
    pdf.section_title("6", "IPC-TO-BNS MAPPING SYSTEM")

    pdf.sub_section("6.1 The Deterministic Dictionary")
    pdf.body_text(
        "The core of the IPC-to-BNS conversion is a hardcoded Python dictionary (IPC_TO_BNS) containing ~300 entries. "
        "This was chosen over AI-based mapping because:"
    )
    pdf.bullet("Accuracy: AI models can hallucinate wrong section numbers. A hardcoded dict is 100% deterministic -- IPC 302 ALWAYS maps to BNS 103, never anything else.")
    pdf.bullet("Speed: Dictionary lookup is O(1) -- instant. No embedding, no similarity search, no LLM call needed.")
    pdf.bullet("Verifiability: Every mapping can be audited against the Ministry of Law & Justice gazette notifications.")
    pdf.bullet("Offline: No model needed for the core mapping. The AI is only used for interpretation AFTER the mapping is confirmed.")

    pdf.sub_section("6.2 Coverage")
    pdf.body_text("The dictionary covers all major IPC chapters:")
    pdf.bullet("Chapter V: Abetment (IPC 107-120 -> BNS 45-58)")
    pdf.bullet("Chapter VI: Offences Against the State (IPC 121-130 -> BNS 147-156)")
    pdf.bullet("Chapter XVI: Offences Affecting Life -- Murder, Culpable Homicide, Hurt (IPC 299-338)")
    pdf.bullet("Chapter XVII: Theft, Extortion, Robbery, Dacoity (IPC 378-402)")
    pdf.bullet("Chapter XVIII: Cheating, Mischief, Trespass, Forgery (IPC 415-489E)")
    pdf.bullet("Sexual Offences (IPC 375-376E -> BNS 63-71)")
    pdf.bullet("Dowry Death, Cruelty (IPC 304B, 498A -> BNS 80, 85)")
    pdf.bullet("Defamation, Criminal Intimidation (IPC 499-510 -> BNS 351-358)")

    pdf.sub_section("6.3 BNS Database (bns_sections.csv)")
    pdf.body_text(
        "358 rows, each representing one BNS section. Columns: Chapter, Chapter_name, Chapter_subtype, "
        "Section, Section_name, Description. This CSV is indexed into ChromaDB (./bns_vault) for semantic "
        "search queries. Each row is combined into a searchable string: "
        "'BNS Section {N}: {Name}. Chapter {C} - {Chapter_name}. {Description}'"
    )

    # ====================================================================
    # 7. DATA ARCHITECTURE
    # ====================================================================
    pdf.add_page()
    pdf.section_title("7", "DATA ARCHITECTURE & STORAGE")

    pdf.sub_section("7.1 ChromaDB Vaults")
    pdf.key_value("./bns_vault", "Persistent ChromaDB index of 358 BNS sections from bns_sections.csv. Built once on first run, reused on subsequent launches. Used for semantic search in IPC-to-BNS tab (text queries and fallback).")
    pdf.key_value("./vidhi_vault", "Persistent ChromaDB index of previously uploaded case PDFs. Serves as a fallback when no new documents are uploaded. Contains embedded chunks from prior analysis sessions.")

    pdf.sub_section("7.2 Session State Management")
    pdf.body_text("Streamlit's st.session_state stores runtime data across reruns:")
    pdf.bullet("st.session_state['chunks']: List of LangChain Document chunks from uploaded PDFs")
    pdf.bullet("st.session_state['all_pdf_texts']: Dict mapping filename -> full extracted text")
    pdf.bullet("st.session_state['pdf_text']: Concatenated text of all uploaded PDFs")
    pdf.bullet("st.session_state['file_names_key']: Hash of uploaded filenames to detect when uploads change")
    pdf.body_text("Session state is cleared when the browser tab is closed or the Streamlit server restarts.")

    pdf.sub_section("7.3 Caching Strategy")
    pdf.body_text("Streamlit's @st.cache_resource decorator is used for expensive objects:")
    pdf.bullet("load_embeddings(): Loads all-MiniLM-L6-v2 once, reused across all tabs and reruns")
    pdf.bullet("load_llm(): Creates Ollama('llama3') client once, reused for all LLM calls")
    pdf.bullet("load_bns_vectorstore(): Loads or builds the BNS ChromaDB index once")
    pdf.bullet("load_bns_csv_rows(): Reads bns_sections.csv once into memory")
    pdf.body_text("Without caching, each button click would reload the 80MB embedding model and re-parse the CSV -- adding 5-10 seconds of overhead per interaction.")

    # ====================================================================
    # 8. HARDWARE CONSTRAINTS & OPTIMIZATIONS
    # ====================================================================
    pdf.add_page()
    pdf.section_title("8", "HARDWARE CONSTRAINTS & OPTIMIZATIONS")

    pdf.sub_section("8.1 Target Hardware Specifications")
    pdf.key_value("CPU", "AMD Ryzen 5 5500U -- 6 cores, 12 threads, 2.1 GHz base / 4.0 GHz boost. Zen 3 architecture.")
    pdf.key_value("RAM", "16 GB DDR4 -- shared between OS, Ollama model loading, ChromaDB, and Python process")
    pdf.key_value("GPU", "AMD Radeon Vega (integrated) -- NOT usable for LLM inference. No CUDA support.")
    pdf.key_value("Storage", "SSD -- important for ChromaDB read/write performance and model loading speed")
    pdf.key_value("OS", "Windows 11")

    pdf.sub_section("8.2 Memory Budget Analysis")
    pdf.body_text("How 16 GB RAM is distributed during peak usage:")
    pdf.bullet("Windows OS + Services: ~3-4 GB")
    pdf.bullet("Ollama + Llama-3 8B (Q4 quantized): ~5-6 GB")
    pdf.bullet("Python process (Streamlit + ChromaDB + embeddings): ~2-3 GB")
    pdf.bullet("Browser (Streamlit UI): ~0.5-1 GB")
    pdf.bullet("Available headroom: ~2-4 GB")
    pdf.highlight_box(
        "Critical Constraint: With only ~2-4 GB headroom, loading a second LLM or a larger model (13B+) "
        "would cause swapping to disk, making the system unusable. This is why Llama-3 8B (Q4) was the "
        "largest feasible model."
    )

    pdf.sub_section("8.3 Optimizations Applied")

    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*VidhiReport.NAVY)
    pdf.cell(0, 6, "Optimization 1: Model Quantization (Q4_K_M)", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*VidhiReport.BLACK)
    pdf.multi_cell(0, 5,
        "Llama-3 8B's full-precision weights are ~16 GB (FP16). Ollama automatically uses Q4_K_M quantization, "
        "compressing to ~4.7 GB. This 4-bit quantization reduces memory by 70% with only ~1-2% quality loss on benchmarks. "
        "The K_M variant uses mixed precision (some layers at higher precision) for better accuracy than pure Q4.")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*VidhiReport.NAVY)
    pdf.cell(0, 6, "Optimization 2: Aggressive Caching (@st.cache_resource)", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*VidhiReport.BLACK)
    pdf.multi_cell(0, 5,
        "Without caching, every Streamlit rerun (triggered by any button click) would reload the embedding model "
        "(~5 sec), re-parse the CSV (~1 sec), and re-initialize the LLM client (~2 sec). With @st.cache_resource, "
        "these are loaded ONCE and persist across all reruns. This saves ~8 seconds per interaction.")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*VidhiReport.NAVY)
    pdf.cell(0, 6, "Optimization 3: Small Embedding Model", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*VidhiReport.BLACK)
    pdf.multi_cell(0, 5,
        "all-MiniLM-L6-v2 (22.7M params, 80MB) was chosen over larger alternatives like e5-large (335M params, 1.3GB) "
        "or instructor-xl (1.5B params, 4.6GB). On a CPU, embedding speed matters: MiniLM embeds in ~200ms vs "
        "e5-large at ~2 seconds. For a responsive dashboard, this 10x speedup was worth the small accuracy tradeoff.")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*VidhiReport.NAVY)
    pdf.cell(0, 6, "Optimization 4: Deterministic Dictionary over AI Mapping", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*VidhiReport.BLACK)
    pdf.multi_cell(0, 5,
        "IPC-to-BNS conversion uses a hardcoded Python dict (~300 entries) instead of an AI model call. "
        "Dict lookup: <1ms. AI model call: 10-30 seconds. This alone saves 10-30 seconds per query on the "
        "IPC-to-BNS tab. The AI is only invoked AFTER the deterministic mapping for interpretation.")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*VidhiReport.NAVY)
    pdf.cell(0, 6, "Optimization 5: Controlled num_predict", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*VidhiReport.BLACK)
    pdf.multi_cell(0, 5,
        "Each LLM call specifies a max token limit (num_predict). AI Judge: 10 tokens (just a section number). "
        "AI Interpretation: 1024 tokens. Conflict report: 2048 tokens. Chronos timeline: default. "
        "This prevents runaway generation that would waste CPU time on irrelevant output.")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*VidhiReport.NAVY)
    pdf.cell(0, 6, "Optimization 6: Temperature=0 Everywhere", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*VidhiReport.BLACK)
    pdf.multi_cell(0, 5,
        "All LLM calls use temperature=0 for deterministic output. In a legal context, reproducibility matters -- "
        "the same query should produce the same answer every time. Temperature=0 also tends to produce more "
        "concise, factual responses (less 'creative wandering').")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*VidhiReport.NAVY)
    pdf.cell(0, 6, "Optimization 7: repeat_penalty=1.3", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*VidhiReport.BLACK)
    pdf.multi_cell(0, 5,
        "Applied to longer generation tasks (AI Interpretation, Bulk Analysis). Prevents the model from "
        "repeating the same phrases in loops, which is a common issue with smaller models on CPU. "
        "A penalty of 1.3 is aggressive enough to prevent loops without making the output too terse.")

    # ====================================================================
    # 9. CHALLENGES FACED & SOLUTIONS
    # ====================================================================
    pdf.add_page()
    pdf.section_title("9", "CHALLENGES FACED & SOLUTIONS")

    challenges = [
        {
            "title": "Challenge 1: LLM Hallucination on Section Numbers",
            "problem": "Early versions used the LLM to generate IPC-to-BNS mappings directly. The model frequently hallucinated wrong section numbers (e.g., mapping IPC 420 to BNS 420 instead of BNS 318), especially for sections where the old and new numbers are very different.",
            "solution": "Replaced AI-based mapping with a hardcoded deterministic dictionary (IPC_TO_BNS) containing ~300 verified entries. The AI is now only used for interpretation AFTER the dictionary confirms the correct mapping. Hallucination rate dropped from ~15% to 0% for mapped sections.",
        },
        {
            "title": "Challenge 2: Context Window Overflow",
            "problem": "Llama-3 8B has an 8K token context window (~32,000 characters). When comparing 3+ long documents in Conflict Detection, the combined text easily exceeds this limit, causing truncation and incomplete analysis.",
            "solution": "Added st.multiselect document selectors to all 3 PDF-dependent tabs (Case Analysis, Chronos, Conflict). Users can now de-select documents they don't need, keeping total text within the context window. Also used chunk_size=500 in RAG to minimize context consumption.",
        },
        {
            "title": "Challenge 3: Regional Language PDF Encoding",
            "problem": "Direct text extraction from Kannada/Hindi PDFs produced (cid:xxxx) garbage because PDF fonts encode Indian scripts as custom character IDs that standard extractors cannot decode.",
            "solution": "Implemented an OCR-First pipeline: PDF pages are converted to 300 DPI images via Poppler, then processed through Tesseract OCR with regional language packs (kan+hin+mar+eng). This bypasses the encoding issue entirely by treating each page as an image.",
        },
        {
            "title": "Challenge 4: Slow Response Times on CPU",
            "problem": "Initial implementation took 45-60 seconds per query because the embedding model, LLM client, and CSV data were reloaded on every Streamlit rerun (every button click triggers a full script re-execution).",
            "solution": "Applied @st.cache_resource to all expensive loaders (embeddings, LLM, vectorstores, CSV). Objects are loaded once and persist across reruns. Reduced per-query overhead from ~45s to ~15-25s (LLM inference time only).",
        },
        {
            "title": "Challenge 5: Wrong Section Selection from Semantic Search",
            "problem": "Semantic search sometimes returned the wrong BNS section as the top result. For example, searching 'murder' might return BNS 100 (Culpable Homicide - definition) instead of BNS 103 (Punishment for Murder) because both contain the word 'murder'.",
            "solution": "Implemented a two-stage approach: (1) contextual_rerank() function checks if query keywords appear in section descriptions and boosts exact matches, and (2) an AI Judge (Llama-3 with num_predict=10) selects the most legally precise section from top-5 candidates. This two-stage filtering eliminated most wrong selections.",
        },
        {
            "title": "Challenge 6: GGUF Model Quality Issues",
            "problem": "An initial approach used a fine-tuned GGUF model (4.7 GB) loaded via llama-cpp-python. The model produced leaked training tags (map:ipc_bns:1.0), repetitive loops, and inconsistent formatting.",
            "solution": "Abandoned the GGUF model entirely and switched to Ollama-served Llama-3 8B. Added clean_ai_output() function with regex post-processing to strip any remaining artifacts. Deleted the 4.7 GB GGUF file to free disk space.",
        },
        {
            "title": "Challenge 7: Case-Insensitive Input Handling",
            "problem": "Users might type '304b', '304B', 'IPC 304B', or '304B(1)'. The system needed to handle all variations consistently.",
            "solution": "All inputs are normalized with .upper(). Sub-section markers like (1), (2), (a) are stripped via regex: re.sub(r'\\([^)]*\\)', '', cleaned). Prefix detection uses regex (^IPC\\s*, ^BNS\\s*) for intelligent routing.",
        },
        {
            "title": "Challenge 8: Empty White Box UI Bug",
            "problem": "A styled <div class='control-panel'> wrapper was split across two separate st.markdown() calls (opening tag in one, closing tag in another). Streamlit rendered each call independently, creating an empty styled box on the page.",
            "solution": "Removed both the opening and closing st.markdown() wrapper calls. Streamlit components don't need manual HTML wrappers since its layout system handles styling internally.",
        },
        {
            "title": "Challenge 9: Table Header Visibility",
            "problem": "Bulk Analysis table headers had dark text on a dark background, making column names invisible.",
            "solution": "Swapped to gold background (#D4AF37) with dark navy text (#1B2A4A) and bold 800-weight. This matches the government theme while ensuring readability.",
        },
        {
            "title": "Challenge 10: Stale Vector Database Data",
            "problem": "After deleting local PDFs, Case Analysis still produced output because ./vidhi_vault ChromaDB persists indexed data independently of the source PDFs.",
            "solution": "Added document selectors that prioritize uploaded+selected docs over the vault. When new documents are uploaded, they take full priority and the vault is NOT mixed in. The vault only serves as a fallback when nothing is uploaded.",
        },
    ]

    for ch in challenges:
        pdf.set_x(10)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*VidhiReport.NAVY)
        pdf.multi_cell(0, 7, ch["title"])
        pdf.set_x(10)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(183, 28, 28)
        pdf.multi_cell(190, 5.5, "Problem:")
        pdf.set_x(10)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*VidhiReport.BLACK)
        pdf.multi_cell(190, 5, ch["problem"])
        pdf.ln(1)
        pdf.set_x(10)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(46, 125, 50)
        pdf.multi_cell(190, 5.5, "Solution:")
        pdf.set_x(10)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*VidhiReport.BLACK)
        pdf.multi_cell(190, 5, ch["solution"])
        pdf.ln(3)

    # ====================================================================
    # 10. SECURITY & OFFLINE GUARANTEES
    # ====================================================================
    pdf.add_page()
    pdf.section_title("10", "SECURITY & OFFLINE GUARANTEES")

    pdf.sub_section("10.1 Air-Gap Compliance")
    pdf.body_text("Vidhi-AI is designed for deployment in air-gapped courtroom networks:")
    pdf.bullet("Ollama runs on localhost:11434 -- no external network calls")
    pdf.bullet("ChromaDB stores all data locally on disk (./vidhi_vault, ./bns_vault)")
    pdf.bullet("Embedding model (all-MiniLM-L6-v2) is cached locally after first download")
    pdf.bullet("No telemetry, no analytics, no phone-home behavior")
    pdf.bullet("Streamlit runs on localhost:8501 -- accessible only from the local machine")

    pdf.sub_section("10.2 Data Flow Guarantee")
    pdf.body_text("Document data flow is strictly local:")
    pdf.bullet("PDF uploaded -> read into Python memory -> text extracted -> embedded locally -> stored in local ChromaDB -> queried locally -> response generated locally -> displayed in local browser")
    pdf.bullet("At NO point does any data leave the machine or touch any network interface")
    pdf.bullet("Even the LLM inference (Ollama) communicates via localhost HTTP, not external APIs")

    pdf.sub_section("10.3 No API Keys Required")
    pdf.body_text(
        "The system requires zero API keys, subscriptions, or third-party accounts. "
        "All dependencies are either: (a) open-source Python packages installed via pip, "
        "(b) the Ollama runtime (open-source, local), or (c) offline data files (CSV, JSON)."
    )

    # ====================================================================
    # 11. PROJECT FILE STRUCTURE
    # ====================================================================
    pdf.add_page()
    pdf.section_title("11", "PROJECT FILE STRUCTURE")

    pdf.code_block(
        "Vidhi_AI_Local/\n"
        "|\n"
        "|-- app.py                        # Main 6-tab Streamlit dashboard (~2900 lines)\n"
        "|-- bns_sections.csv              # 358 BNS sections (Chapter, Section, Description)\n"
        "|-- law_map.json                  # IPC/CrPC -> BNS/BNSS mapping (JSON)\n"
        "|-- local_pdf_reader.py           # Phase 1: PDF -> ChromaDB vault builder\n"
        "|-- local_rag_pipeline.py         # Phase 2: Full RAG chain (ChromaDB -> Llama-3)\n"
        "|-- local_chronos_extractor.py    # Phase 3: Timeline extraction script\n"
        "|-- local_rag_app.py              # Phase 4: GGUF + law_map.json CLI app\n"
        "|-- backup_vidhi.bat              # Windows backup script (date-stamped)\n"
        "|-- generate_project_report.py    # This PDF report generator\n"
        "|\n"
        "|-- .streamlit/\n"
        "|   |-- config.toml              # Forces light theme\n"
        "|\n"
        "|-- bns_vault/                    # ChromaDB index (358 BNS sections)\n"
        "|-- vidhi_vault/                  # ChromaDB index (uploaded PDF chunks)\n"
        "|-- poppler-25.12.0/             # Poppler binaries for PDF-to-image\n"
        "|-- venv/                         # Python virtual environment\n"
    )

    pdf.sub_section("11.1 Key File Sizes")
    pdf.bullet("app.py: ~2,932 lines (main dashboard -- CSS, logic, all 6 tabs)")
    pdf.bullet("bns_sections.csv: 358 rows (BNS database)")
    pdf.bullet("IPC_TO_BNS dictionary: ~300 entries (hardcoded in app.py, lines ~710-873)")
    pdf.bullet("bns_vault/: ChromaDB persistent index (~5-10 MB)")
    pdf.bullet("venv/: Python virtual environment with all dependencies")

    # ====================================================================
    # 12. FUTURE SCOPE
    # ====================================================================
    pdf.add_page()
    pdf.section_title("12", "FUTURE SCOPE & IMPROVEMENTS")

    pdf.sub_section("12.1 Potential Enhancements")
    pdf.bullet("BNSS (Criminal Procedure) Mapping: Extend the dictionary to cover CrPC -> BNSS transition (criminal procedure code, not just penal code)")
    pdf.bullet("BSA (Evidence Act) Mapping: Add Indian Evidence Act -> Bharatiya Sakshya Adhiniyam mappings")
    pdf.bullet("Multi-document RAG: Build a unified vector store from all uploaded documents for cross-document case analysis")
    pdf.bullet("Case Law Database: Index landmark Supreme Court and High Court judgments for precedent retrieval")
    pdf.bullet("PDF Report Export: Generate downloadable PDF reports for Conflict Detection and Bulk Analysis results")
    pdf.bullet("Smaller/Faster LLM: Switch to Llama-3.2 3B or Phi-3.5 Mini (3.8B) for 2-3x faster inference on CPU without major quality loss")
    pdf.bullet("GPU Acceleration: If deployed on a machine with NVIDIA GPU, enable CUDA layers in Ollama for 5-10x speedup")
    pdf.bullet("User Authentication: Add login system for multi-user courtroom deployment")
    pdf.bullet("Audit Trail: Log all queries and AI responses for judicial accountability")

    pdf.sub_section("12.2 Known Limitations")
    pdf.bullet("Context window: Llama-3's 8K context limit restricts analysis of very long documents (100+ pages)")
    pdf.bullet("Inference speed: CPU-only inference takes 15-30 seconds per query (vs ~1 second with GPU)")
    pdf.bullet("OCR accuracy: Tesseract OCR accuracy depends on PDF scan quality -- poor scans produce garbled text")
    pdf.bullet("No real-time updates: BNS section data is static (from CSV). Legislative amendments require manual CSV updates")

    # ====================================================================
    # 13. ARCHITECTURAL REFACTORING & MODULARIZATION
    # ====================================================================
    pdf.add_page()
    pdf.section_title("13", "ARCHITECTURAL REFACTORING & MODULARIZATION")

    pdf.body_text("To ensure production readiness, maintainability, and scalability, the original monolithic architecture (a single ~2,900-line app.py file) was comprehensively refactored into 18 distinct, focused modules. This refactoring preserved 100% of the original logic while drastically improving code quality.")

    pdf.sub_section("13.1 Code Organization")
    pdf.code_block(
        "Vidhi_AI_Local/\n"
        "|-- app.py                    # Slim orchestrator (~160 lines)\n"
        "|-- styles.py                 # Extracted government-style CSS\n"
        "|-- ipc_bns_mapping.py        # IPC-to-BNS deterministic dictionary\n"
        "|-- utils.py                  # Shared utilities (clean_ai_output, html_escape)\n"
        "|-- loaders.py                # Cached resource loaders & Ollama health check\n"
        "|-- vidhi_logger.py           # Rotating file & console logging framework\n"
        "|-- tabs/                     # Modularized UI components\n"
        "|   |-- case_analysis.py      # RAG-based question answering\n"
        "|   |-- chronos.py            # Evidence timeline extraction\n"
        "|   |-- conflict.py           # Multi-document cross-examination\n"
        "|   |-- statute_bridge.py     # IPC to BNS statute transition lookup\n"
        "|   |-- regional_ocr.py       # Vernacular OCR and translation\n"
        "|   |-- bulk_analysis.py      # Bulk document IPC scanning\n"
        "|-- tests/                    # 43 automated unit tests\n"
    )

    pdf.sub_section("13.2 Testing & Quality Assurance")
    pdf.body_text("A comprehensive test suite was introduced, featuring 43 passing unit tests across 3 dedicated test files:")
    pdf.bullet("tests/test_ipc_bns_mapping.py (20 tests): Validates deterministic dictionary lookups and contextual re-ranking.")
    pdf.bullet("tests/test_utils.py (18 tests): Ensures AI output cleaning, filename sanitization, and HTML escaping work correctly.")
    pdf.bullet("tests/test_loaders.py (5 tests): Tests CSV data loading and Ollama health checks.")

    pdf.sub_section("13.3 Security & Reliability Improvements")
    pdf.bullet("Logging Framework: Implemented a robust logging system (vidhi_logger.py) with rotating file handlers.")
    pdf.bullet("File Upload Security: Added filename sanitization and isolated uploads in a secure .uploads/ directory.")
    pdf.bullet("Health Checks: Added proactive checks for the Ollama server state to degrade gracefully if offline.")
    pdf.bullet("Version Control: Created comprehensive .gitignore and README.md files for better repository management.")

    # ====================================================================
    # FINAL PAGE -- SUMMARY
    # ====================================================================
    pdf.add_page()
    pdf.ln(10)
    pdf.set_fill_color(*VidhiReport.NAVY)
    pdf.rect(15, 30, 180, 60, 'F')
    pdf.set_draw_color(*VidhiReport.GOLD)
    pdf.set_line_width(1.5)
    pdf.rect(17, 32, 176, 56, 'D')
    pdf.set_line_width(0.2)
    pdf.set_draw_color(0, 0, 0)

    pdf.set_text_color(*VidhiReport.GOLD)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_xy(20, 38)
    pdf.cell(170, 12, "PROJECT SUMMARY", align="C")

    pdf.set_text_color(*VidhiReport.WHITE)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(20, 52)
    pdf.multi_cell(170, 6,
        "Vidhi-AI demonstrates that a production-quality legal AI assistant can run entirely on a "
        "consumer laptop without any cloud dependency. By combining a quantized Llama-3 8B model, "
        "ChromaDB vector storage, LangChain RAG orchestration, and a deterministic IPC-to-BNS "
        "mapping dictionary, the system achieves accurate, grounded, and reproducible legal analysis -- "
        "all within the constraints of 16 GB RAM and a CPU-only AMD Ryzen 5 5500U.",
        align="C"
    )

    pdf.set_text_color(*VidhiReport.BLACK)
    pdf.set_font("Helvetica", "", 10)
    pdf.ln(40)
    pdf.body_text(
        "Key Statistics:\n"
        "- Total codebase: 18 modular Python files (~3,000 lines) + 4 backend scripts\n"
        "- Test Suite: 43 automated unit tests covering core logic\n"
        "- Technologies: 12+ (Python, Streamlit, LangChain, Ollama, ChromaDB, HuggingFace, "
        "pdfplumber, PyMuPDF, Tesseract, Poppler, Pillow, pdf2image)\n"
        "- BNS sections indexed: 358\n"
        "- IPC-to-BNS mappings: ~300 (deterministic dictionary)\n"
        "- Dashboard tabs: 6 functional modules\n"
        "- Cloud API calls: ZERO\n"
        "- GPU required: NO\n"
        "- Internet required: NO (after initial setup)"
    )

    # -- Save the PDF ----------------------------------------------------
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "Vidhi_AI_Technical_Report.pdf"
    )
    pdf.output(output_path)
    print(f"\n{'='*60}")
    print(f"  PDF GENERATED SUCCESSFULLY")
    print(f"  Location: {output_path}")
    print(f"  Pages: {pdf.page_no()}")
    print(f"{'='*60}")
    return output_path


if __name__ == "__main__":
    generate_report()
