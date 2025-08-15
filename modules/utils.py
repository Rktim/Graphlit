# graphlit/modules/utils.py
import os
import uuid
import streamlit as st
import pandas as pd

# ---------- Session / Theme ----------
def init_session():
    st.session_state.setdefault("df_raw", None)
    st.session_state.setdefault("df_clean", None)
    st.session_state.setdefault("dashboard", [])  # [{id,title,fig/png_bytes/html,meta}]
    st.session_state.setdefault("global_filters", {})  # {col: selected_values or (min,max)}
    st.session_state.setdefault("settings", {"engine":"plotly"})

def load_theme(path: str):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- IDs / Keys ----------
def uid() -> str:
    return uuid.uuid4().hex

# ---------- Data I/O (cached) ----------
@st.cache_data(show_spinner=False)
def read_csv_cached(file) -> pd.DataFrame:
    return pd.read_csv(file)

@st.cache_data(show_spinner=False)
def read_excel_cached(file) -> pd.DataFrame:
    return pd.read_excel(file)

@st.cache_data(show_spinner=False)
def read_sql_cached(sql: str, conn_str: str) -> pd.DataFrame:
    from sqlalchemy import create_engine
    engine = create_engine(conn_str)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)

# ---------- Column typing helpers ----------
def numeric_cols(df):     return df.select_dtypes(include=["number"]).columns.tolist()
def categorical_cols(df): return df.select_dtypes(include=["object","category","bool"]).columns.tolist()
def datetime_cols(df):    return df.select_dtypes(include=["datetime64[ns]","datetimetz"]).columns.tolist()

def coerce_datetimes(df: pd.DataFrame) -> pd.DataFrame:
    # Try soft parse of date-like columns
    for c in df.columns:
        if df[c].dtype == "object":
            smpl = df[c].astype(str).head(30)
            if smpl.str.contains(r"\d{4}-\d{1,2}-\d{1,2}|/|:").mean() > .3:
                try: df[c] = pd.to_datetime(df[c], errors="ignore", infer_datetime_format=True)
                except Exception: pass
    return df

# ---------- Smart field suggestions ----------
def smart_field_options(df: pd.DataFrame, chart_type: str, force_all: bool = False):
    """
    Returns only relevant X and Y columns for a chart type.
    If force_all=True, returns all columns.
    Only falls back to all columns if there is truly no match.
    """
    if df is None or df.empty:
        return [], []

    if force_all:
        all_cols = df.columns.tolist()
        return all_cols, all_cols

    nums = numeric_cols(df)
    cats = categorical_cols(df)
    dates = datetime_cols(df)

    if chart_type in ("Bar", "Line", "Multi-metric"):
        x_opts = list(dict.fromkeys(cats + dates))
        y_opts = nums
    elif chart_type == "Scatter":
        x_opts = nums
        y_opts = nums
    elif chart_type == "Pie":
        x_opts = cats
        y_opts = nums
    elif chart_type == "Histogram":
        x_opts = nums
        y_opts = []
    elif chart_type == "Box":
        x_opts = cats
        y_opts = nums
    elif chart_type == "Heatmap":
        x_opts = nums
        y_opts = []
    else:
        x_opts = df.columns.tolist()
        y_opts = df.columns.tolist()

    # Strict mode — only fallback if no matches at all
    if not x_opts:
        x_opts = df.columns.tolist()
    if not y_opts:
        y_opts = df.columns.tolist()

    return x_opts, y_opts

# ---------- Safer calc expressions ----------
ALLOWED_FUNCS = {"abs":abs,"round":round}
def safe_calc(df: pd.DataFrame, expr: str) -> pd.Series:
    """
    Safe-ish column calculator: allows arithmetic with existing columns and a tiny
    whitelist of python builtins. Blocks access to names outside allowed scope.
    Example: '(Revenue - Cost) / Cost'
    """
    local_dict = {c: df[c] for c in df.columns}
    local_dict.update(ALLOWED_FUNCS)
    # pandas.eval is vectorized & prevents attribute access; still restrict names
    return pd.eval(expr, engine="python", parser="pandas", local_dict=local_dict)

# ---------- Global filters ----------
def apply_global_filters(df: pd.DataFrame) -> pd.DataFrame:
    flt = st.session_state.get("global_filters", {})
    if not flt: return df
    dff = df.copy()
    for c, val in flt.items():
        if c not in dff.columns: continue
        if isinstance(val, tuple) and len(val)==2:  # numeric or datetime range
            lo, hi = val
            dff = dff[(dff[c] >= lo) & (dff[c] <= hi)]
        else:  # set membership
            dff = dff[dff[c].isin(val)]
    return dff
