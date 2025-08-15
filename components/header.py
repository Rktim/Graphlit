# components/header.py
import streamlit as st
import base64

def load_logo_base64(path):
    """Load image file and return as base64 string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def render_header():
    logo_base64 = load_logo_base64("assets/new logo.png")
    st.markdown(
        f"""
        <style>
        .app-header {{
            position: sticky;
            top: 0;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(90deg, #0e1525, #1f2a40);
            padding: 0.6rem 1rem;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 2px 8px rgba(0,0,0,0.35);
        }}
        .app-header img {{
            height: 45px;
            margin-right: 12px;
        }}
        .app-header h1 {{
            font-family: 'Segoe UI', Roboto, sans-serif;
            font-size: 1.6rem;
            color: #f4f7fa;
            margin: 0;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        </style>

        <div class="app-header">
            <img src="data:image/png;base64,{logo_base64}">
        </div>
        """,
        unsafe_allow_html=True
    )
