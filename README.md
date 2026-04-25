# ⚖️ Vidhi-AI — Smart Court Assistant

**100% Offline · Zero Cloud APIs · Air-Gapped Courtroom Ready**

Vidhi-AI is a fully offline, AI-powered legal assistant designed for the Indian judicial system. It runs entirely on a consumer laptop (16 GB RAM, CPU-only) using a local Llama-3 8B model via Ollama — no internet, no API keys, no cloud dependency.

---

## ✨ Features

| Module | Description |
|---|---|
| **Case Analysis** | RAG-based question answering over uploaded legal PDFs |
| **Chronos** | Automated chronological timeline extraction from evidence |
| **Conflict Detection** | Multi-document cross-examination for evidentiary contradictions |
| **IPC → BNS Statute Bridge** | Deterministic IPC-to-BNS mapping + AI-powered semantic search |
| **Regional OCR** | Vernacular PDF processing (Kannada, Hindi, Marathi) with translation |
| **Bulk Analysis** | Automated IPC section scanning and BNS transition reporting |

---

## 🛠️ Tech Stack

- **LLM**: Llama-3 8B (Q4 quantized) via [Ollama](https://ollama.com/)
- **RAG**: LangChain + ChromaDB + HuggingFace Embeddings (all-MiniLM-L6-v2)
- **Frontend**: Streamlit with custom government-style CSS theme
- **OCR**: Tesseract OCR + Poppler (PDF-to-image conversion)
- **PDF Processing**: pdfplumber + PyMuPDF (fallback)
- **Language**: Python 3.10+

---

## 📋 Prerequisites

1. **Python 3.10+** — [Download](https://www.python.org/downloads/)
2. **Ollama** — [Download](https://ollama.com/download)
3. **Tesseract OCR** — [Download](https://github.com/UB-Mannheim/tesseract/wiki)
   - Install with language packs: `eng`, `kan`, `hin`, `mar`
4. **Poppler** — [Download](https://github.com/oschwartz10612/poppler-windows/releases)
   - Add `bin/` folder to system PATH

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd Vidhi_AI_Local

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Pull Llama-3 model
ollama pull llama3
```

---

## ▶️ Usage

```bash
# 1. Start Ollama (in a separate terminal)
ollama serve

# 2. Run the dashboard
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`.

---

## 📁 Project Structure

```
Vidhi_AI_Local/
├── app.py                        # Main orchestrator (~160 lines)
├── styles.py                     # Government-style CSS theme
├── ipc_bns_mapping.py            # Deterministic IPC→BNS dictionary + helpers
├── utils.py                      # Shared utilities (clean, sanitize, escape)
├── loaders.py                    # Cached resource loaders + Ollama health check
├── vidhi_logger.py               # Logging configuration
├── tabs/
│   ├── case_analysis.py          # Tab 1: RAG-based Case Analysis
│   ├── chronos.py                # Tab 2: Timeline Extraction
│   ├── conflict.py               # Tab 3: Evidence Conflict Detection
│   ├── statute_bridge.py         # Tab 4: IPC→BNS Statute Bridge
│   ├── regional_ocr.py           # Tab 5: Vernacular OCR + Translation
│   └── bulk_analysis.py          # Tab 6: Bulk Document Analysis
├── tests/
│   ├── test_ipc_bns_mapping.py   # Unit tests for IPC→BNS mapping
│   ├── test_utils.py             # Unit tests for utility functions
│   └── test_loaders.py           # Unit tests for data loaders
├── bns_sections.csv              # 358 BNS sections database
├── law_map.json                  # IPC/CrPC → BNS/BNSS mapping (JSON)
├── requirements.txt              # Python dependencies
├── .streamlit/config.toml        # Streamlit theme configuration
├── .gitignore                    # Version control exclusions
└── README.md                     # This file
```

---

## 🔒 Security & Privacy

- **100% Offline**: No data ever leaves the machine
- **Air-Gap Compliant**: Runs on `localhost` only — no network calls
- **Zero API Keys**: No external accounts or subscriptions required
- **Secure Uploads**: Filenames are sanitized; uploads stored in `.uploads/`

---

## ⚙️ System Requirements

| Component | Minimum |
|---|---|
| RAM | 16 GB |
| CPU | 4+ cores (e.g., AMD Ryzen 5 5500U) |
| GPU | Not required (CPU-only inference) |
| Disk | ~10 GB (model + dependencies) |
| OS | Windows 10/11, Linux, macOS |

---

## 📝 License

This project is for educational and research purposes.

---

*Built for the Indian Judiciary — Secure, Offline, Trustworthy.*
