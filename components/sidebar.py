# graphlit/components/sidebar.py
import streamlit as st
from PIL import Image
from modules.preprocessing import load_data_ui, cleaning_ui
from modules.utils import numeric_cols, categorical_cols, datetime_cols

LOGO_CANDIDATES = ["new logo.png","graphlit_logo_transparent.png","graphlit.png","logo.png"]

def _load_logo():
    for p in LOGO_CANDIDATES:
        try:
            return Image.open(p)
        except Exception:
            continue
    return None

def global_filters_ui():
    st.markdown("### 3 • Global filters (apply to all charts)")
    df = st.session_state.df_clean
    if df is None: return
    flt_state = st.session_state.get("global_filters", {})

    cats = categorical_cols(df)
    nums = numeric_cols(df) + datetime_cols(df)

    with st.expander("Categorical filters", expanded=False):
        for c in cats[:25]:  # avoid huge UIs
            vals = sorted(map(str, df[c].dropna().unique().tolist()))[:200]
            if not vals: continue
            selected = st.multiselect(f"{c}", vals, default=flt_state.get(c, []))
            if selected: flt_state[c] = selected
            elif c in flt_state: del flt_state[c]

    with st.expander("Numeric/Date ranges", expanded=False):
        for c in nums[:25]:
            try:
                lo, hi = df[c].min(), df[c].max()
                val = st.slider(f"{c}", min_value=lo, max_value=hi, value=flt_state.get(c,(lo,hi)))
                flt_state[c] = val
            except Exception:
                pass

    st.session_state.global_filters = flt_state

def render_sidebar():
    st.title("GraphLit")
    st.caption("Smart data visualization")

    logo = _load_logo()
    if logo is not None:
        st.image(logo, use_container_width=True)

    load_data_ui()
    cleaning_ui()
    global_filters_ui()

    st.markdown("---")
    st.caption("Created by Raktim • GitHub: https://github.com/Rktim")
