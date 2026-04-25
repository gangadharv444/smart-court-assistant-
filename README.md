# ⚖️ Vidhi-AI — Smart Court Assistant

**100% Offline · Zero Cloud APIs · Air-Gapped Courtroom Ready**

Vidhi-AI is a fully offline, AI-powered legal assistant designed for the Indian judicial system. It runs entirely on a consumer laptop (16 GB RAM, CPU-only) using a local Llama-3 8B model via Ollama — no internet, no API keys, no cloud dependency.

**Solves a critical problem:** FIRs contain sensitive witness names, addresses, victim details. Traditional legal AI sends this to OpenAI/Google → confidentiality breach. Vidhi-AI runs 100% locally. Your data NEVER leaves your judge's machine.

---

## 🎥 See It In Action

**[Watch Demo Video (3 min)](https://github.com/gangadharv444/smart-court-assistant-/raw/main/smart_court_assistant.mp4)** — Shows real FIR analysis, timeline extraction, and conflict detection.

---

## ✨ Features

| Feature | What It Does |
|---------|-------------|
| **Case Analysis** | Upload FIR → Ask questions → AI answers grounded in document (RAG-based) |
| **Chronos** | Automatically extract chronological timeline of events from evidence |
| **Conflict Detection** | Cross-examine 2+ FIRs for contradictions in facts, timelines, witness accounts |
| **IPC → BNS Bridge** | Map any IPC section to new BNS equivalent (300+ deterministic mappings) |
| **Regional OCR** | Extract text from Kannada/Hindi/Marathi PDFs with English translation |
| **Bulk Analysis** | Auto-scan PDFs for all IPC sections, generate BNS transition report |

---

## 🚀 Quick Start

### 1️⃣ Prerequisites (5 min)

Install these once:

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Ollama** — [Download](https://ollama.com/download)
- **Tesseract OCR** — [Download](https://github.com/UB-Mannheim/tesseract/wiki)
  - During install, select language packs: `English`, `Kannada`, `Hindi`, `Marathi`
- **Poppler** — [Download](https://github.com/oschwartz10612/poppler-windows/releases/)
  - Download the `.zip`, extract it, add `bin/` folder to Windows PATH

### 2️⃣ Clone & Setup (10 min)

```bash
# Clone the repo
git clone https://github.com/gangadharv444/smart-court-assistant-
cd smart-court-assistant-

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start Ollama (in separate terminal)
ollama run llama2
# This downloads Llama-3 8B (5 GB) on first run — takes 5-10 minutes
```

### 3️⃣ Run the App (1 min)

```bash
# In the original terminal:
streamlit run app.py

# Opens browser automatically at http://localhost:8501
```

### 4️⃣ Try Sample FIRs (2 min)

The repo includes dummy PDFs:
- `dummy_fir.pdf` — Sample FIR
- `witness_statement.pdf` — Witness statement
- `orfir.pdf` — Another FIR for conflict detection

**Try these:**
1. Go to **Case Analysis** tab
2. Upload `dummy_fir.pdf`
3. Ask: *"What is the timeline of events?"* or *"What crimes are mentioned?"*
4. Go to **Conflict Detection** tab
5. Upload both `dummy_fir.pdf` and `orfir.pdf`
6. Click "Analyze" to see contradictions

---

## 🛠️ Tech Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| **LLM** | Llama-3 8B (Q4 quantized) via Ollama | Runs on CPU, no GPU needed, 8K context window |
| **RAG** | LangChain + ChromaDB + HuggingFace Embeddings | Fast semantic search, local storage, deterministic |
| **Frontend** | Streamlit | No frontend code needed, hot-reload, built-in file upload |
| **OCR** | Tesseract + Poppler | Handles Indian scripts (Kannada, Hindi, Marathi) |
| **PDF Processing** | pdfplumber + PyMuPDF | Dual extraction for max compatibility |
| **Language** | Python 3.10+ | Rich ML/NLP ecosystem |

---

## 📋 System Requirements

| Component | Minimum |
|-----------|---------|
| **RAM** | 16 GB (Ollama: 5-6 GB, Python: 2-3 GB, OS: 3-4 GB) |
| **CPU** | 6+ cores recommended (tested on AMD Ryzen 5 5500U) |
| **GPU** | None — CPU-only inference |
| **Storage** | 20 GB (Ollama model + dependencies + ChromaDB indexes) |
| **OS** | Windows 10/11, macOS 12+, Linux (Ubuntu 20+) |

---

## 📁 Project Structure

```
smart-court-assistant-/
├── app.py                          # Main Streamlit dashboard (6 tabs)
├── tabs/                           # Modular UI components
│   ├── case_analysis.py           # RAG-based Q&A
│   ├── chronos.py                 # Timeline extraction
│   ├── conflict.py                # Multi-doc conflict detection
│   ├── statute_bridge.py           # IPC → BNS mapping
│   ├── regional_ocr.py             # Vernacular OCR + translation
│   └── bulk_analysis.py            # Bulk IPC scanning
├── ipc_bns_mapping.py              # Deterministic IPC↔BNS dictionary
├── loaders.py                      # Cached resource loaders
├── styles.py                       # Government-style CSS theme
├── utils.py                        # Helper functions
├── vidhi_logger.py                 # Logging framework
├── bns_sections.csv                # 358 BNS sections database
├── requirements.txt                # Python dependencies
├── dummy_fir.pdf                   # Sample FIR (for testing)
├── witness_statement.pdf           # Sample witness statement
├── orfir.pdf                       # Sample FIR #2 (conflict testing)
└── Vidhi_AI_Technical_Report.pdf   # Full technical documentation
```

---

## 🔒 Security & Privacy

✅ **100% Offline** — No internet calls after initial setup
✅ **Zero Cloud APIs** — Ollama runs locally on port 11434
✅ **Air-Gapped Ready** — Works on isolated court networks
✅ **No Telemetry** — No analytics, no phone-home behavior
✅ **Local Storage** — All embeddings & indexes on disk (./vidhi_vault, ./bns_vault)

**Data Flow:**
```
PDF Upload → Local Text Extraction → Local Embedding → Local ChromaDB → Local LLM (Ollama) → Browser Display
```

Every step happens on your machine. Nothing leaves.

---

## 📊 Key Statistics

- **Codebase:** 18 modular Python files, ~3,000 lines
- **Tests:** 43 unit tests covering core logic
- **BNS Sections Indexed:** 358 (complete database)
- **IPC-to-BNS Mappings:** ~300 (100% deterministic, zero hallucination)
- **Dashboard Tabs:** 6 functional modules
- **Cloud API Calls:** ZERO
- **GPU Required:** NO
- **Internet Required:** NO (after initial setup)

---

## 🚨 Troubleshooting

### "Ollama not found"
```bash
# Make sure Ollama is running in a separate terminal:
ollama run llama2
```

### "Tesseract not found" (OCR tab)
1. Download [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
2. During install, select English + regional languages
3. Add install path to Windows PATH (usually `C:\Program Files\Tesseract-OCR\bin`)
4. Restart Streamlit

### "Poppler not found" (PDF to image conversion)
1. Download [Poppler Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
2. Extract the `.zip` file
3. Copy the path to `poppler-xx.x.x\Library\bin`
4. Add to Windows PATH
5. Restart Streamlit

### App runs but models are slow
- First inference takes 30-45 seconds (model loading from disk)
- Subsequent queries: 15-25 seconds
- This is normal on CPU — consider using GPU for production

---

## 📚 Documentation

- **[Technical Report](./Vidhi_AI_Technical_Report.pdf)** — Deep dive into architecture, RAG pipeline, optimizations
- **[IPC-BNS Mapping](./ipc_bns_mapping.py)** — Full dictionary of 300+ legal transitions
- **[API Reference](./docs/API.md)** — (Coming soon)

---

## 🤝 Contributing

Want to help? We need:

1. **Test with Real Court Networks** — Deploy on intranet, report issues
2. **Improve Regional Language OCR** — Better Marathi/Tamil/Telugu support
3. **Add BNSS Mapping** — Criminal Procedure code transitions (CrPC → BNSS)
4. **UI/UX Improvements** — Make it easier for non-technical judges
5. **Bug Fixes** — Report issues, submit PRs

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## 📝 License

MIT License — See [LICENSE](./LICENSE) for details.

You can use, modify, and distribute this freely (even commercially) as long as you include the original license.

---

## 🙋 Questions?

- **Technical Issues?** Open a [GitHub Issue](https://github.com/gangadharv444/smart-court-assistant-/issues)
- **Want to Deploy?** Email: [your-email@example.com](mailto:your-email@example.com)
- **Feedback?** DM [@gangadharv444](https://github.com/gangadharv444)

---

## 🎯 Roadmap

- [ ] BNSS (Criminal Procedure) mapping
- [ ] Case law database (Supreme Court judgments)
- [ ] Docker image for easy deployment
- [ ] Web interface for cloud deployment (optional, secure)
- [ ] Mobile app (React Native)
- [ ] Multi-user support with audit logs

---

**Built with ❤️ for the Indian Judiciary**

*Making justice faster, fairer, and more secure.*
