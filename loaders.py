# ============================================================
# Vidhi-AI | Cached Resource Loaders
# ============================================================

import streamlit as st
import os
import csv
import httpx
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from vidhi_logger import logger

# Import Ollama — compatible with both old and new langchain versions
try:
    from langchain_community.llms import Ollama
except ImportError:
    from langchain_ollama import OllamaLLM as Ollama


# =============================================================================
# Ollama Health Check
# =============================================================================
def check_ollama_health() -> bool:
    """Check if Ollama server is running on localhost:11434.
    Returns True if reachable, False otherwise."""
    try:
        resp = httpx.get("http://localhost:11434/api/tags", timeout=3.0)
        if resp.status_code == 200:
            logger.info("Ollama server is reachable.")
            return True
    except (httpx.ConnectError, httpx.TimeoutException, OSError) as e:
        logger.warning("Ollama server is not reachable: %s", e)
    return False


# =============================================================================
# Cached Resource Loaders
# =============================================================================
@st.cache_resource(show_spinner=False)
def load_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


@st.cache_resource(show_spinner=False)
def load_llm():
    return Ollama(model="llama3")


@st.cache_resource(show_spinner=False)
def load_bns_vectorstore(_embeddings):
    """Load or build a ChromaDB index from bns_sections.csv."""
    bns_vault_path = "./bns_vault"
    csv_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "bns_sections.csv",
    )

    # If the vault already exists, just load it
    if os.path.exists(bns_vault_path) and os.listdir(bns_vault_path):
        return Chroma(
            persist_directory=bns_vault_path,
            embedding_function=_embeddings,
            collection_name="bns_sections",
        )

    # Build the vault from CSV
    docs = []
    metadatas = []
    ids = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            section = row.get("Section", "").strip()
            section_name = row.get("Section _name", "").strip()
            description = row.get("Description", "").strip()
            chapter = row.get("Chapter", "").strip()
            chapter_name = row.get("Chapter_name", "").strip()

            # Combine into a searchable document
            combined = (
                f"BNS Section {section}: {section_name}. "
                f"Chapter {chapter} - {chapter_name}. "
                f"{description}"
            )

            docs.append(combined)
            metadatas.append({
                "section": section,
                "section_name": section_name,
                "chapter": chapter,
                "chapter_name": chapter_name,
                "description": description,
            })
            ids.append(f"bns_{idx}")

    vectorstore = Chroma.from_texts(
        texts=docs,
        embedding=_embeddings,
        metadatas=metadatas,
        ids=ids,
        persist_directory=bns_vault_path,
        collection_name="bns_sections",
    )
    logger.info("Built BNS vectorstore with %d sections.", len(docs))
    return vectorstore


@st.cache_data(show_spinner=False)
def load_bns_csv_rows():
    """Load all rows from bns_sections.csv into a list of dicts."""
    csv_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "bns_sections.csv",
    )
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "section": row.get("Section", "").strip(),
                "section_name": row.get("Section _name", "").strip(),
                "description": row.get("Description", "").strip(),
                "chapter": row.get("Chapter", "").strip(),
                "chapter_name": row.get("Chapter_name", "").strip(),
            })
    return rows


@st.cache_resource(show_spinner=False)
def load_vectorstore(_embeddings):
    return Chroma(
        persist_directory="./vidhi_vault",
        embedding_function=_embeddings,
    )
