# Contributing to Vidhi-AI

Thank you for your interest in improving Vidhi-AI! We welcome contributions from developers, legal professionals, and anyone passionate about making AI tools for the Indian judiciary.

---

## 🎯 What We Need Help With (Priority Order)

### 🔴 High Priority

**1. Real-World Testing**
- Deploy Vidhi-AI on a court intranet
- Test with actual FIRs (redacted)
- Report stability issues, edge cases, performance problems
- We'll credit you as a tester

**2. BNSS Mapping (Criminal Procedure Code)**
- Indian courts need CrPC → BNSS transitions
- Similar to IPC → BNS (which we have)
- Create `crpc_bnss_mapping.json` with ~200+ entries
- Use official Ministry of Law gazette as reference
- Contact us if you have legal expertise

**3. Regional Language Support**
- Improve OCR accuracy for Marathi, Tamil, Telugu, Bengali
- Test Tesseract + Poppler pipeline with real regional documents
- Fine-tune language packs
- Contribute better translation prompts

### 🟡 Medium Priority

**4. UI/UX Improvements**
- Make the dashboard more intuitive for non-technical judges
- Improve mobile responsiveness
- Add export features (PDF reports, Word docs)
- Better error messages for users

**5. Performance Optimization**
- Test on lower-spec laptops (8GB RAM, 4-core CPU)
- Profile the RAG pipeline, find bottlenecks
- Implement model quantization improvements
- Cache optimization

### 🟢 Low Priority

**6. Documentation**
- Write deployment guides for specific courts
- Create video tutorials
- Translate docs to Hindi/regional languages
- Add more examples

---

## 🔧 How to Contribute

### Step 1: Fork & Clone

```bash
# Fork the repo on GitHub (click "Fork" button)
# Then clone your fork:
git clone https://github.com/YOUR-USERNAME/smart-court-assistant-
cd smart-court-assistant-

# Add upstream (to stay in sync)
git remote add upstream https://github.com/gangadharv444/smart-court-assistant-
```

### Step 2: Create a Feature Branch

```bash
# Always work on a new branch (never on main)
git checkout -b feature/your-feature-name

# Good branch names:
# - feature/bnss-mapping
# - bugfix/ocr-marathi-crash
# - docs/deployment-guide
# - test/court-network-validation
```

### Step 3: Make Your Changes

**For code changes:**
```bash
# 1. Make your changes
# 2. Test locally:
python -m pytest tests/

# 3. Check code style:
pip install black flake8
black --line-length 100 your_file.py
flake8 your_file.py
```

**For documentation changes:**
- Keep markdown simple and clear
- Use tables for comparisons
- Add code examples where relevant
- Update README.md if it affects users

### Step 4: Commit & Push

```bash
# Commit with clear message
git commit -m "Add BNSS mapping for CrPC sections 100-500"

# Push to your fork
git push origin feature/your-feature-name
```

### Step 5: Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Fill in the template:

```markdown
## What does this PR do?
Brief description of changes

## Why?
What problem does it solve?

## Type of change
- [ ] Bugfix
- [ ] New feature
- [ ] Documentation
- [ ] Testing
- [ ] Performance improvement

## Testing
How did you test this? Any edge cases?

## Screenshots/Demo (if applicable)
Include video or images

## Checklist
- [ ] Code follows style guidelines (black, flake8)
- [ ] Tests pass (pytest)
- [ ] No new warnings
- [ ] Changes are documented
```

---

## 📋 Contribution Guidelines

### Code Style

We follow **PEP 8** with these rules:

```python
# ✅ Good
def extract_timeline_from_fir(pdf_path: str) -> list[dict]:
    """Extract chronological timeline from FIR.
    
    Args:
        pdf_path: Path to FIR PDF file
        
    Returns:
        List of dicts with date, time, event
    """
    timeline = []
    # ... implementation
    return timeline

# ❌ Bad
def extracttimeline(pdf):
    # no docstring
    timeline = []
    return timeline
```

Rules:
- Max line length: 100 characters
- Use type hints: `def func(x: str) -> bool:`
- Document all functions with docstrings
- Use descriptive variable names
- No hardcoded values in code (use config files)

### Testing

Every new feature needs tests:

```python
# tests/test_statute_bridge.py
import pytest
from ipc_bns_mapping import ipc_to_bns

def test_ipc_302_maps_to_bns_103():
    """IPC 302 (murder) should map to BNS 103"""
    result = ipc_to_bns("IPC 302")
    assert result == "BNS 103"

def test_invalid_ipc_returns_none():
    """Invalid IPC section should return None"""
    result = ipc_to_bns("IPC 999")
    assert result is None
```

Run tests:
```bash
pytest tests/
pytest tests/test_statute_bridge.py -v
```

### Commit Messages

```bash
# ✅ Good
git commit -m "Add BNSS mapping for sections 100-250

- Create crpc_bnss_mapping.json with 150 entries
- Update statute_bridge.py to include BNSS lookup
- Add 15 unit tests for new functionality
- Tested with real court documents"

# ❌ Bad
git commit -m "fix stuff"
git commit -m "changes"
```

Format: `Action: What you did [optional detailed explanation]`

### When to Ask Questions

Before starting work on something big:

1. **Check existing issues** — Maybe someone's already working on it
2. **Open a new issue** — Describe what you want to do
3. **Wait for feedback** — We'll tell you if we want it
4. **Then start coding** — Avoid wasted effort

Example issue:
```
Title: Add BNSS mapping for CrPC sections

Description:
The judiciary now uses BNSS instead of CrPC (as of July 2024).
Judges need a way to cross-reference old CrPC sections → new BNSS sections.

Proposal:
- Create crpc_bnss_mapping.json with ~200+ entries
- Add BNSS tab to the dashboard
- Include deterministic lookup (like we did for IPC→BNS)

Questions:
- Should BNSS be in the same tab as IPC-BNS, or separate?
- Do we need AI interpretation for BNSS, or just mappings?
```

---

## 🧪 Testing Strategy

### Unit Tests (Fast, Isolated)

Test individual functions:
```python
# tests/test_ipc_bns_mapping.py
def test_ipc_to_bns():
    assert ipc_to_bns("302") == "BNS 103"
    assert ipc_to_bns("420") == "BNS 318"
```

Run: `pytest tests/`

### Integration Tests (Slow, Real Data)

Test the full pipeline:
```python
# tests/test_rag_pipeline.py
def test_case_analysis_with_dummy_fir():
    """Test RAG on actual dummy_fir.pdf"""
    result = analyze_case("dummy_fir.pdf", "What is the crime?")
    assert "IPC" in result or "BNS" in result
```

Run: `pytest tests/ -v`

### Manual Testing (Required Before PR)

```bash
# 1. Test all 6 tabs work
streamlit run app.py

# 2. Upload sample PDFs
# dummy_fir.pdf, witness_statement.pdf

# 3. Test each feature:
# - Case Analysis: Ask questions
# - Chronos: Extract timeline
# - Conflict Detection: Compare 2 FIRs
# - IPC-BNS: Search for sections
# - Regional OCR: Upload Kannada PDF
# - Bulk Analysis: Scan for IPC sections
```

---

## 🚀 Development Setup

### Full Setup (with testing)

```bash
git clone https://github.com/gangadharv444/smart-court-assistant-
cd smart-court-assistant-

python -m venv venv
venv\Scripts\activate

# Install dependencies + dev tools
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Start Ollama (separate terminal)
ollama run llama2

# Run tests
pytest tests/ -v --cov=.

# Format code
black --line-length 100 *.py tabs/ tests/
```

### What to Install Before Contributing

```bash
pip install -r requirements.txt  # Core dependencies
pip install pytest               # Testing
pip install black flake8         # Code formatting
pip install pytest-cov          # Test coverage reports
```

---

## 🎁 What You Get (For Contributors)

### Recognition

- Your name in CONTRIBUTORS.md
- GitHub credits (linked to your profile)
- Mention in project updates

### Learning

- Work on real legal AI problems
- Contribute to Indian judiciary tech
- Build experience with LLM/RAG systems
- Network with legal tech professionals

### Proof of Work

- Open-source contributions on GitHub
- Real portfolio piece for job interviews
- Potential legal tech job opportunities

---

## ❓ FAQ

**Q: I'm not a developer. Can I still contribute?**

A: Yes! We need:
- Legal professionals to validate mappings
- Testers to use it with real FIRs
- Translators for regional languages
- UI/UX designers for better layouts

**Q: How long should a PR be?**

A: Small is better:
- 50-200 lines = perfect
- 200-500 lines = good
- 500+ lines = break it into multiple PRs

**Q: Will my contribution be credited?**

A: Yes. Add yourself to `CONTRIBUTORS.md` in your PR.

**Q: What if my PR gets rejected?**

A: That's OK! We'll explain why and how to improve it. Rejection is feedback, not personal.

**Q: How do I stay updated?**

A: Click "Watch" on the GitHub repo to get notifications when we post updates.

---

## 📧 Contact

- **Questions?** Open an issue on GitHub
- **Want to discuss an idea first?** Email: [contact info]
- **Found a security issue?** Email (don't open public issue)

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License (same as the project).

---

**Thank you for helping make Vidhi-AI better! 🙏**
