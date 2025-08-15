import streamlit as st
import pandas as pd

def metric_card(title, value, icon=None, color="#2ecc71"):
    """Creates a styled metric card."""
    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.05);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.08);
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        ">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem; color:{color};">
                {icon if icon else ''}
            </div>
            <div style="font-size: 0.9rem; font-weight: 600; color: #a5b4c0;">{title}</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: white;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def overview_panel(df: pd.DataFrame):
    """Displays structured insights in a visually appealing format."""
    st.subheader("📊 Dataset Overview")

    # Basic dataset stats
    total_rows = len(df)
    total_cols = len(df.columns)
    missing_values = df.isnull().sum().sum()
    duplicated_rows = df.duplicated().sum()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Rows", f"{total_rows:,}", "📄", "#2ecc71")
    with col2:
        metric_card("Total Columns", total_cols, "🧩", "#3498db")
    with col3:
        metric_card("Missing Values", f"{missing_values:,}", "⚠️", "#f39c12")
    with col4:
        metric_card("Duplicate Rows", duplicated_rows, "♻️", "#e74c3c")

    st.markdown("---")

    # Column types
    st.subheader("🔍 Column Summary")
    col_summary = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum(),
        "Unique Values": df.nunique()
    })
    st.dataframe(col_summary, use_container_width=True)

    st.markdown("---")

    # Quick sample preview
    st.subheader("📋 Sample Data")
    st.dataframe(df.head(), use_container_width=True)
