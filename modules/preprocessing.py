# graphlit/modules/preprocessing.py
import streamlit as st
import pandas as pd
from io import StringIO
from modules.utils import read_csv_cached, read_excel_cached, coerce_datetimes, safe_calc

def load_data_ui():
    st.header("1 • Load data")
    tab1, tab2, tab3 = st.tabs(["Upload","Paste CSV","SQL"])
    df = None

    with tab1:
        up = st.file_uploader("Upload CSV or Excel", type=["csv","xlsx"])
        if up:
            try:
                if up.name.lower().endswith(".csv"): df = read_csv_cached(up)
                else: df = read_excel_cached(up)
                st.success(f"Loaded {up.name}  •  Rows: {len(df)}  Cols: {df.shape[1]}")
            except Exception as e:
                st.error(f"Read error: {e}")

    with tab2:
        t = st.text_area("Paste CSV here", height=140, placeholder="col1,col2\n1,2\n3,4")
        if t.strip():
            try:
                df = pd.read_csv(StringIO(t))
                st.success(f"Pasted CSV • Rows: {len(df)}  Cols: {df.shape[1]}")
            except Exception as e:
                st.error(f"Parse error: {e}")

    with tab3:
        st.caption("Tip: supply a SQLAlchemy connection string. Example: "
                   "`postgresql+psycopg2://user:pass@host:5432/db`")
        conn = st.text_input("Connection string")
        sql  = st.text_area("SQL (SELECT only)")
        if st.button("Run SQL") and conn and sql:
            try:
                from modules.utils import read_sql_cached
                df = read_sql_cached(sql, conn)
                st.success(f"Loaded from SQL • Rows: {len(df)}  Cols: {df.shape[1]}")
            except Exception as e:
                st.error(f"SQL error: {e}")

    if df is not None:
        df = coerce_datetimes(df)
        st.session_state.df_raw = df
        st.session_state.df_clean = df.copy()

def cleaning_ui():
    st.header("2 • Quick clean")
    if st.session_state.df_clean is None:
        st.info("Load data first.")
        return

    df = st.session_state.df_clean

    with st.expander("Select columns to keep", expanded=True):
        cols = df.columns.tolist()
        keep = st.multiselect("Keep columns", cols, default=cols, key="keep_cols")
        if not keep:
            st.warning("Select at least one column.")
        else:
            st.session_state.df_clean = df[keep]

    with st.expander("Handle missing values", expanded=False):
        cur = st.session_state.df_clean
        col = st.selectbox("Column", cur.columns)
        method = st.selectbox("Method", ["None","Drop rows","Fill mean","Fill median","Fill mode","Fill custom"])
        if method != "None":
            if method == "Drop rows":
                st.session_state.df_clean = cur.dropna(subset=[col])
            elif method == "Fill mean":
                st.session_state.df_clean[col] = cur[col].fillna(cur[col].mean())
            elif method == "Fill median":
                st.session_state.df_clean[col] = cur[col].fillna(cur[col].median())
            elif method == "Fill mode":
                st.session_state.df_clean[col] = cur[col].fillna(cur[col].mode().iloc[0])
            else:
                val = st.text_input("Custom value")
                if st.button("Apply fill"): st.session_state.df_clean[col] = cur[col].fillna(val)
            st.success("Applied.")

    with st.expander("Rename columns", expanded=False):
        cur = st.session_state.df_clean
        newnames = {}
        for c in cur.columns:
            newnames[c] = st.text_input(f"{c} →", value=c, key=f"rn_{c}")
        if st.button("Apply renames"):
            st.session_state.df_clean = cur.rename(columns=newnames)
            st.success("Renamed.")

    with st.expander("Calculated column (safe)", expanded=False):
        cur = st.session_state.df_clean
        expr = st.text_input("Formula (e.g., (Revenue - Cost) / Cost )")
        name = st.text_input("New column name")
        if st.button("Create column") and expr and name:
            try:
                st.session_state.df_clean[name] = safe_calc(cur, expr)
                st.success(f"Created '{name}'")
            except Exception as e:
                st.error(f"Failed: {e}")
