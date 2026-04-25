# ============================================================
# Vidhi-AI | Government-Style Theme (CSS) — Deep Navy + Gold
# ============================================================

import streamlit as st


def inject_css():
    """Inject the government-style CSS theme into the Streamlit app."""
    st.markdown(CSS, unsafe_allow_html=True)


CSS = """
<style>
    /* --- Root variables — Authority Theme -------------------------------- */
    :root {
        --navy:        #0A1628;
        --navy-mid:    #152238;
        --navy-light:  #1E3050;
        --gold:        #C9A227;
        --gold-light:  #E8C84A;
        --gold-muted:  #A68A1A;
        --cream:       #FDF8EE;
        --warm-white:  #FEFCF7;
        --parchment:   #F5F0E3;
        --sand:        #E8DFC8;
        --text-dark:   #1A1A1A;
        --text-mid:    #3D3D3D;
        --border-warm: #D4C5A9;
        --success:     #2E7D32;
        --white:       #FFFFFF;
    }

    /* --- Force light background on EVERYTHING (override dark mode) ------- */
    html, body, [class*="css"],
    .stApp, [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    .main, .main .block-container,
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="column"] {
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
        color: var(--text-dark) !important;
        background-color: var(--cream) !important;
    }
    .stApp > header {
        background-color: transparent !important;
    }

    /* --- All headings ---------------------------------------------------- */
    h1, h2, h3, h4, h5, h6,
    [data-testid="stHeading"],
    [data-testid="stHeading"] h1,
    [data-testid="stHeading"] h2,
    [data-testid="stHeading"] h3,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
        color: var(--navy) !important;
        font-weight: 700 !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    /* Override: header title must stay gold/white on navy bg */
    .govt-header h1,
    div.govt-header h1,
    .govt-header > h1 {
        color: var(--gold-light) !important;
    }
    .govt-header p,
    div.govt-header p,
    .govt-header > p {
        color: #B0BEC5 !important;
    }

    /* --- All paragraph and span text ------------------------------------- */
    p, span, li, td, th, label {
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
        color: var(--text-dark) !important;
    }
    /* govt-header: force light text on dark bg for ALL children */
    .govt-header, .govt-header * {
        color: #FFFFFF !important;
    }

    /* --- Streamlit markdown text ----------------------------------------- */
    .stMarkdown p {
        font-size: 1rem !important;
        line-height: 1.8 !important;
        color: var(--text-dark) !important;
    }
    .stMarkdown strong {
        color: var(--navy) !important;
    }

    /* --- Hide Streamlit branding ----------------------------------------- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background-color: transparent !important;}

    /* --- Top header bar — deep navy with gold accent -------------------- */
    .govt-header {
        background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 100%) !important;
        color: var(--white) !important;
        padding: 1.8rem 2.5rem;
        border-bottom: 5px solid var(--gold);
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 16px rgba(10, 22, 40, 0.35);
    }
    .govt-header h1 {
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 2.1rem !important;
        font-weight: 700 !important;
        margin: 0;
        letter-spacing: 2px;
        color: var(--gold-light) !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
    }
    .govt-header p {
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1.05rem !important;
        margin: 0.5rem 0 0 0;
        color: #B0BEC5 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* --- Section headers — navy with gold underline ---------------------- */
    .section-header {
        font-family: 'Segoe UI', sans-serif !important;
        color: var(--navy) !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        border-bottom: 3px solid var(--gold);
        padding-bottom: 0.5rem;
        margin-bottom: 1.25rem;
        margin-top: 0.5rem;
        letter-spacing: 0.5px;
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
    }

    /* --- Control panel (left column) ------------------------------------- */
    .control-panel {
        background-color: var(--warm-white) !important;
        border: 2px solid var(--border-warm);
        border-top: 4px solid var(--navy);
        border-radius: 6px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(10, 22, 40, 0.08);
    }
    .control-panel p, .control-panel span, .control-panel label {
        font-size: 0.95rem !important;
        color: var(--text-dark) !important;
    }

    /* --- Result card ----------------------------------------------------- */
    .result-card {
        background-color: var(--warm-white) !important;
        border: 2px solid var(--border-warm);
        border-left: 6px solid var(--gold);
        border-radius: 6px;
        padding: 1.5rem 1.75rem;
        margin-top: 1.25rem;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1.05rem !important;
        color: var(--text-dark) !important;
        line-height: 1.9;
        white-space: pre-wrap;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(10, 22, 40, 0.06);
    }

    /* --- Status badge ---------------------------------------------------- */
    .status-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--success) 0%, #388E3C 100%) !important;
        color: var(--white) !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 700;
        padding: 0.45rem 1rem;
        border-radius: 4px;
        margin-bottom: 0.75rem;
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }

    /* --- Info labels in control panel ------------------------------------ */
    .info-label {
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1rem !important;
        color: var(--text-dark) !important;
        margin: 0.3rem 0;
        line-height: 1.7;
    }
    .info-label strong {
        color: var(--navy) !important;
    }

    /* --- System status table --------------------------------------------- */
    .status-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 0.5rem;
        font-family: 'Segoe UI', sans-serif !important;
    }
    .status-table th {
        background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 100%) !important;
        color: var(--gold-light) !important;
        font-size: 0.95rem !important;
        font-weight: 700;
        padding: 0.7rem 0.85rem;
        text-align: left;
        border: 1px solid var(--navy);
        letter-spacing: 0.5px;
    }
    .status-table td {
        font-size: 0.95rem !important;
        padding: 0.65rem 0.85rem;
        border: 1px solid var(--border-warm);
        color: var(--text-dark) !important;
        background-color: var(--warm-white) !important;
    }
    .status-table tr:nth-child(even) td {
        background-color: var(--parchment) !important;
    }

    /* --- Footer ---------------------------------------------------------- */
    .govt-footer {
        text-align: center;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 0.85rem !important;
        color: var(--text-mid) !important;
        background-color: var(--parchment) !important;
        margin-top: 3rem;
        padding: 1.25rem 0;
        border-top: 3px solid var(--navy);
        letter-spacing: 0.3px;
        line-height: 1.6;
    }

    /* --- Button overrides — navy with gold hover ------------------------- */
    .stButton > button {
        background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 100%) !important;
        color: var(--gold-light) !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border: 2px solid var(--gold-muted) !important;
        border-radius: 5px !important;
        padding: 0.75rem 1.25rem !important;
        letter-spacing: 0.5px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 2px 8px rgba(10, 22, 40, 0.2) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 100%) !important;
        color: var(--navy) !important;
        border-color: var(--gold) !important;
        box-shadow: 0 4px 12px rgba(201, 162, 39, 0.3) !important;
    }
    .stButton > button:active {
        background-color: var(--gold-muted) !important;
        color: var(--navy) !important;
    }
    .stButton > button p, .stButton > button span {
        color: inherit !important;
    }

    /* --- Input field styling --------------------------------------------- */
    .stTextInput > div > div > input {
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1rem !important;
        color: var(--text-dark) !important;
        background-color: var(--white) !important;
        border: 2px solid var(--border-warm) !important;
        border-radius: 5px !important;
        padding: 0.65rem 0.85rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 3px rgba(201, 162, 39, 0.2) !important;
    }
    .stTextInput label {
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: var(--navy) !important;
    }

    /* --- File uploader styling ------------------------------------------- */
    .stFileUploader label {
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: var(--navy) !important;
    }
    .stFileUploader section {
        border: 2px dashed var(--gold-muted) !important;
        border-radius: 6px !important;
        background-color: var(--parchment) !important;
    }
    .stFileUploader section span, .stFileUploader section p,
    .stFileUploader section small, .stFileUploader section div {
        color: var(--text-dark) !important;
    }
    .stFileUploader button {
        background-color: var(--navy) !important;
        color: var(--gold-light) !important;
        border: 1px solid var(--gold-muted) !important;
        border-radius: 4px !important;
    }

    /* --- Tab styling ----------------------------------------------------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 3px solid var(--navy);
        background-color: transparent !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 700;
        color: var(--text-mid) !important;
        background-color: var(--parchment) !important;
        padding: 0.75rem 2rem;
        border-radius: 6px 6px 0 0;
        border: 1px solid var(--border-warm) !important;
        border-bottom: none !important;
        margin-right: 4px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--navy) !important;
        background-color: var(--sand) !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--navy) !important;
        background-color: var(--warm-white) !important;
        border-bottom: 4px solid var(--gold) !important;
        border-color: var(--navy) !important;
        border-bottom-color: var(--gold) !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: var(--cream) !important;
    }

    /* --- Spinner text ---------------------------------------------------- */
    .stSpinner > div > span {
        font-size: 1rem !important;
        color: var(--navy) !important;
        font-weight: 600;
    }

    /* --- Warning / Info boxes -------------------------------------------- */
    .stAlert {
        background-color: var(--parchment) !important;
        border: 1px solid var(--border-warm) !important;
    }
    .stAlert p, .stAlert span {
        color: var(--text-dark) !important;
        font-size: 0.95rem !important;
    }

    /* --- Scrollbar styling ----------------------------------------------- */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--parchment);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--border-warm);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--gold-muted);
    }

    /* --- Small helper text / captions ------------------------------------ */
    small, .stCaption, [data-testid="stCaptionContainer"] {
        color: var(--text-mid) !important;
        font-size: 0.85rem !important;
    }

    /* --- Responsive: mobile adjustments ---------------------------------- */
    @media (max-width: 768px) {
        .govt-header h1 { font-size: 1.5rem !important; color: var(--gold-light) !important; }
        .govt-header p { font-size: 0.85rem !important; }
        .section-header { font-size: 1.1rem !important; }
        .result-card { padding: 1rem 1.25rem; font-size: 1rem !important; }
        .stTabs [data-baseweb="tab"] { padding: 0.6rem 1rem; font-size: 0.95rem !important; }
    }

    /* --- FINAL OVERRIDE: header text must always be visible -------------- */
    .govt-header h1,
    .stMarkdown .govt-header h1,
    div.govt-header h1,
    [data-testid="stMarkdownContainer"] .govt-header h1 {
        color: #FFFFFF !important;
        font-size: 2.1rem !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5) !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    .govt-header p,
    .stMarkdown .govt-header p,
    div.govt-header p,
    [data-testid="stMarkdownContainer"] .govt-header p {
        color: #B0BEC5 !important;
        font-size: 1.05rem !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    /* Button text override */
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: var(--gold-light) !important;
    }
    .stButton > button:hover p,
    .stButton > button:hover span,
    .stButton > button:hover div {
        color: var(--navy) !important;
    }

    /* --- Conflict Audit Report Styles ------------------------------------ */
    .audit-banner-red {
        background-color: #B71C1C !important;
        color: #FFFFFF !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 0.85rem 1.25rem;
        border-radius: 5px;
        letter-spacing: 1px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 1.25rem;
        border: 2px solid #7F0000;
    }
    .audit-banner-green {
        background-color: #1B5E20 !important;
        color: #FFFFFF !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 0.85rem 1.25rem;
        border-radius: 5px;
        letter-spacing: 1px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 1.25rem;
        border: 2px solid #0D3B0D;
    }
    .audit-report {
        background-color: var(--warm-white) !important;
        border: 2px solid var(--navy);
        border-top: 5px solid var(--navy);
        border-radius: 6px;
        padding: 2rem 2.25rem;
        margin-top: 1rem;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1rem !important;
        color: var(--text-dark) !important;
        line-height: 1.9;
        box-shadow: 0 3px 12px rgba(10, 22, 40, 0.1);
    }
    .audit-report-title {
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: var(--navy) !important;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        border-bottom: 3px double var(--navy);
        padding-bottom: 0.75rem;
        margin-bottom: 1.25rem;
    }
    .conflict-item {
        background-color: #FFF5F5 !important;
        border: 1px solid #E53935;
        border-left: 5px solid #B71C1C;
        border-radius: 4px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1rem !important;
        color: var(--text-dark) !important;
        line-height: 1.7;
    }
    .conflict-item strong {
        color: #B71C1C !important;
    }
    .conflict-label {
        display: inline-block;
        background-color: #B71C1C !important;
        color: #FFFFFF !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 3px;
        margin-bottom: 0.4rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .observation-box {
        background-color: var(--parchment) !important;
        border: 1px solid var(--border-warm);
        border-left: 5px solid var(--gold);
        border-radius: 4px;
        padding: 1rem 1.25rem;
        margin-top: 1rem;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 1rem !important;
        color: var(--text-dark) !important;
        line-height: 1.8;
    }

    /* --- Regional Language Support Tab ----------------------------------- */
    .lang-column-header {
        background-color: var(--navy) !important;
        color: var(--white) !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.75rem 1rem;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-radius: 4px 4px 0 0;
        margin-bottom: 0;
    }
    .lang-text-box {
        background-color: var(--warm-white) !important;
        border: 1px solid var(--border-warm);
        border-top: none;
        border-radius: 0 0 4px 4px;
        padding: 1.25rem;
        min-height: 200px;
        max-height: 500px;
        overflow-y: auto;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 0.95rem !important;
        color: var(--text-dark) !important;
        line-height: 1.8;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .lang-info-badge {
        display: inline-block;
        background-color: var(--gold) !important;
        color: var(--navy) !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 700;
        padding: 0.25rem 0.75rem;
        border-radius: 3px;
        margin: 0.25rem 0.25rem 0.5rem 0;
        letter-spacing: 0.5px;
    }
</style>
"""
