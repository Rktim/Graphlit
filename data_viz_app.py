# graphlit/app.py
import streamlit as st
from components.sidebar import render_sidebar
from components.main_tab import render_main
from modules.utils import init_session, load_theme
from components.header import render_header  # ⬅️ Import new header

# 1️⃣ Must be first Streamlit command
st.set_page_config(page_title="GraphLit", layout="wide", page_icon="📊")

# 2️⃣ Load theme & session
load_theme("assets/style.css")
init_session()

# 3️⃣ Render sticky header
render_header()

# 4️⃣ Sidebar
with st.sidebar:
    render_sidebar()

# 5️⃣ Main content
render_main()
