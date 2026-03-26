import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>

        /* ========= GLOBAL APP ========= */
        .stApp,
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #e9f7ff 0%, #fff7b8 100%) !important;
            color: #5a4f68 !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        [data-testid="stToolbar"] {
            right: 1rem;
        }

        [data-testid="stMainBlockContainer"] {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1200px !important;
        }

        /* ========= SIDEBAR ========= */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffdbe8 0%, #ffeaf2 100%) !important;
            border-right: 1px solid #f4bfd0 !important;
        }

        [data-testid="stSidebarContent"] {
            background: transparent !important;
        }

        [data-testid="stSidebar"] * {
            color: #6a5667 !important;
        }

        /* ========= TYPOGRAPHY ========= */
        .main-title {
            font-size: 2.6rem;
            font-weight: 800;
            color: #5c4c73;
            margin-bottom: 0.3rem;
            line-height: 1.15;
        }

        .sub-title {
            font-size: 1.08rem;
            color: #6f687f;
            margin-bottom: 1.5rem;
        }

        .section-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #5c4c73;
            margin-bottom: 0.75rem;
        }

        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: #5a4f68;
        }

        /* ========= CARDS ========= */
        .soft-card {
            background: rgba(255, 255, 255, 0.68) !important;
            border: 1px solid rgba(255, 225, 160, 0.95) !important;
            border-radius: 22px !important;
            padding: 1.2rem 1.2rem 1rem 1.2rem !important;
            box-shadow: 0 10px 24px rgba(133, 130, 170, 0.10) !important;
            backdrop-filter: blur(7px);
            margin-bottom: 1rem;
        }

        .mini-card {
            background: rgba(255, 255, 255, 0.72) !important;
            border: 1px solid rgba(255, 215, 145, 0.85) !important;
            border-radius: 18px !important;
            padding: 1rem !important;
            box-shadow: 0 8px 18px rgba(133, 130, 170, 0.08) !important;
            text-align: center;
            margin-bottom: 0.75rem;
        }

        .metric-number {
            font-size: 1.8rem;
            font-weight: 800;
            color: #5d4d74;
        }

        .metric-label {
            font-size: 0.92rem;
            color: #7a728a;
        }

        /* ========= TAG PILLS ========= */
        .pill {
            display: inline-block;
            background: #ffd8e8;
            color: #8b4d68 !important;
            padding: 0.28rem 0.7rem;
            border-radius: 999px;
            margin: 0.15rem 0.3rem 0.15rem 0;
            font-size: 0.85rem;
            font-weight: 700;
            border: 1px solid #f6bdd1;
        }

        /* ========= INPUTS ========= */
        .stTextInput input,
        .stTextArea textarea {
            background: #fffdf8 !important;
            color: #5a4f68 !important;
            border: 1px solid #f1d79d !important;
            border-radius: 16px !important;
        }

        div[data-baseweb="select"] > div {
            background: #fffdf8 !important;
            color: #5a4f68 !important;
            border: 1px solid #f1d79d !important;
            border-radius: 16px !important;
        }

        /* ========= BUTTONS ========= */
        .stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #ffc7db 0%, #ffe98d 100%) !important;
            color: #5c4c73 !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 0.75rem 1rem !important;
            font-weight: 800 !important;
            box-shadow: 0 6px 14px rgba(255, 196, 214, 0.28) !important;
        }

        .stButton > button:hover {
            filter: brightness(1.03);
            transform: translateY(-1px);
            transition: 0.2s ease;
        }

        /* ========= DELETE BUTTON ========= */
        .stButton > button[kind="secondary"] {
            background: #ffe5ea !important;
            color: #a64b68 !important;
            border: 1px solid #f3b6c6 !important;
        }

        /* ========= SEGMENTED CONTROL ========= */
        div[data-testid="stSegmentedControl"] button {
            border-radius: 12px !important;
            background: rgba(255,255,255,0.7) !important;
            color: #5a4f68 !important;
            font-weight: 600 !important;
            border: 1px solid #f2d6df !important;
            padding: 0.4rem 0.8rem !important;
        }

        div[data-testid="stSegmentedControl"] button[aria-pressed="true"] {
            background: linear-gradient(90deg, #ffc7db 0%, #ffe98d 100%) !important;
            color: #5c4c73 !important;
            font-weight: 700 !important;
        }

        /* ========= EXPANDERS ========= */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.55) !important;
            border-radius: 14px !important;
        }

        /* ========= ALERTS ========= */
        .stAlert {
            border-radius: 16px !important;
        }

        /* ========= DISABLED TEXT ========= */
        textarea:disabled {
            background: rgba(255, 252, 245, 0.8) !important;
            color: #6a6075 !important;
        }

        /* ========= DIVIDER ========= */
        .soft-divider {
            height: 1px;
            background: linear-gradient(
                90deg,
                rgba(255,199,219,0),
                rgba(255,199,219,0.8),
                rgba(255,233,141,0.8),
                rgba(255,199,219,0)
            );
            border: none;
            margin: 1rem 0 1.2rem 0;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )