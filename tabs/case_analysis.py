# ============================================================
# Vidhi-AI | Tab 1: Case Analysis (RAG)
# ============================================================

import streamlit as st
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from loaders import load_embeddings, load_llm, load_vectorstore
from vidhi_logger import logger


def render():
    """Render the Case Analysis (RAG) tab."""
    st.markdown(
        '<div class="section-header">Judicial Case Analysis</div>',
        unsafe_allow_html=True,
    )

    # Document selector for Case Analysis
    _case_docs = st.session_state.get("all_pdf_texts", {})
    _case_doc_names = list(_case_docs.keys())

    if _case_doc_names:
        selected_case_docs = st.multiselect(
            "Select documents to analyze:",
            options=_case_doc_names,
            default=_case_doc_names,
            help="Choose which uploaded PDFs to include in the analysis.",
            key="case_doc_selector",
        )
    else:
        selected_case_docs = []

    query = st.text_input(
        "Enter your legal query:",
        value="Based on the FIR, detail the crime, the suspect, and the time.",
        help="Ask any question about the uploaded legal document.",
    )

    run_analysis = st.button(
        "Submit Query for Analysis",
        use_container_width=True,
        key="btn_case",
    )

    if run_analysis and query:
        with st.spinner("Processing query through local RAG pipeline..."):
            embeddings = load_embeddings()
            llm = load_llm()

            # Build vectorstore from selected documents only
            if selected_case_docs and _case_docs:
                from langchain_core.documents import Document as LCDocument
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500, chunk_overlap=50
                )
                selected_chunks = []
                for doc_name in selected_case_docs:
                    doc_text = _case_docs.get(doc_name, "")
                    if not doc_text.strip():
                        continue
                    doc_obj = LCDocument(
                        page_content=doc_text,
                        metadata={"source": doc_name},
                    )
                    selected_chunks.extend(
                        splitter.split_documents([doc_obj])
                    )

                if not selected_chunks:
                    st.warning("No readable text found in the selected documents. Please verify your PDFs.")
                    st.stop()

                vectorstore = Chroma.from_documents(
                    documents=selected_chunks,
                    embedding=embeddings,
                )
            elif "chunks" in st.session_state and st.session_state["chunks"]:
                vectorstore = Chroma.from_documents(
                    documents=st.session_state["chunks"],
                    embedding=embeddings,
                )
            else:
                vectorstore = load_vectorstore(embeddings)

            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

            system_prompt = (
                "You are an Indian Legal Assistant. "
                "Answer the question based strictly on the provided context.\n\n"
                "Context:\n{context}"
            )
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}"),
            ])

            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            rag_chain = (
                {
                    "context": retriever | format_docs,
                    "input": RunnablePassthrough(),
                }
                | prompt
                | llm
                | StrOutputParser()
            )

            answer = rag_chain.invoke(query)
            logger.info("Case analysis query completed: %s", query[:80])

        st.markdown(
            '<div class="section-header">Analysis Result</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="result-card">{answer}</div>',
            unsafe_allow_html=True,
        )
