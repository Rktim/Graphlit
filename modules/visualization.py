import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from modules.utils import uid

# ==============================
# Utility — Add chart to dashboard
# ==============================
def add_to_dashboard(fig, title, meta=None):
    """Add a chart to the dashboard stored in session state."""
    if "dashboard" not in st.session_state:
        st.session_state.dashboard = []

    try:
        st.session_state.dashboard.append({
            "id": uid(),
            "title": title or "Chart",
            "fig": fig,
            "metadata": meta or {}
        })
        st.success(f"✅ Added '{title}' to Dashboard")
    except Exception as e:
        st.error(f"Failed to add chart: {e}")

# ==============================
# Chart functions
# ==============================

def bar_chart(df, preset, palette, title, rotate_x, dtick, yfmt, showlegend, agg, group_by):
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    category_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

    x = st.selectbox("X axis", category_cols, key="bar_x")
    y = st.selectbox("Y axis", numeric_cols, key="bar_y")

    fig = px.bar(df, x=x, y=y, color=group_by, color_discrete_sequence=palette,
                 title=title if title else None)
    fig.update_layout(showlegend=showlegend)
    fig.update_xaxes(tickangle=rotate_x, dtick=dtick if dtick != 0 else None)
    if yfmt:
        fig.update_yaxes(tickformat=yfmt)

    st.plotly_chart(fig, use_container_width=True)

    if st.button("➕ Add to Dashboard", key="bar_add"):
        add_to_dashboard(fig, title or f"Bar Chart ({x} vs {y})")

def line_chart(df, preset, palette, title, rotate_x, dtick, yfmt, showlegend, agg, group_by):
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    category_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

    x = st.selectbox("X axis", category_cols, key="line_x")
    y = st.selectbox("Y axis", numeric_cols, key="line_y")

    fig = px.line(df, x=x, y=y, color=group_by, color_discrete_sequence=palette,
                  title=title if title else None)
    fig.update_layout(showlegend=showlegend)
    fig.update_xaxes(tickangle=rotate_x, dtick=dtick if dtick != 0 else None)
    if yfmt:
        fig.update_yaxes(tickformat=yfmt)

    st.plotly_chart(fig, use_container_width=True)

    if st.button("➕ Add to Dashboard", key="line_add"):
        add_to_dashboard(fig, title or f"Line Chart ({x} vs {y})")

def scatter_chart(df, preset, palette, title, rotate_x, dtick, yfmt, showlegend, agg, group_by):
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    x = st.selectbox("X axis", numeric_cols, key="scatter_x")
    y = st.selectbox("Y axis", numeric_cols, key="scatter_y")

    fig = px.scatter(df, x=x, y=y, color=group_by, color_discrete_sequence=palette,
                     title=title if title else None)
    fig.update_layout(showlegend=showlegend)
    fig.update_xaxes(tickangle=rotate_x, dtick=dtick if dtick != 0 else None)
    if yfmt:
        fig.update_yaxes(tickformat=yfmt)

    st.plotly_chart(fig, use_container_width=True)

    if st.button("➕ Add to Dashboard", key="scatter_add"):
        add_to_dashboard(fig, title or f"Scatter Chart ({x} vs {y})")

def pie_chart(df, preset, palette, title):
    category_cols = df.select_dtypes(exclude=["number"]).columns.tolist()
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    names = st.selectbox("Labels", category_cols, key="pie_labels")
    values = st.selectbox("Values", numeric_cols, key="pie_values")

    fig = px.pie(df, names=names, values=values, color_discrete_sequence=palette,
                 title=title if title else None)

    st.plotly_chart(fig, use_container_width=True)

    if st.button("➕ Add to Dashboard", key="pie_add"):
        add_to_dashboard(fig, title or f"Pie Chart ({names})")

def histogram(df, preset, palette, title, yfmt):
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    x = st.selectbox("Histogram Variable", numeric_cols, key="hist_x")

    fig = px.histogram(df, x=x, color_discrete_sequence=palette,
                       title=title if title else None)
    if yfmt:
        fig.update_yaxes(tickformat=yfmt)

    st.plotly_chart(fig, use_container_width=True)

    if st.button("➕ Add to Dashboard", key="hist_add"):
        add_to_dashboard(fig, title or f"Histogram ({x})")

def box_plot(df, preset, palette, title):
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    category_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

    y = st.selectbox("Y axis", numeric_cols, key="box_y")
    x = st.selectbox("X axis", category_cols, key="box_x")

    fig = px.box(df, x=x, y=y, color=x, color_discrete_sequence=palette,
                 title=title if title else None)

    st.plotly_chart(fig, use_container_width=True)

    if st.button("➕ Add to Dashboard", key="box_add"):
        add_to_dashboard(fig, title or f"Box Plot ({x} vs {y})")

def heatmap(df, preset, palette, title):
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    if len(numeric_cols) < 2:
        st.warning("Need at least two numeric columns for heatmap.")
        return

    corr = df[numeric_cols].corr()

    fig = px.imshow(corr, text_auto=True, color_continuous_scale=palette,
                    title=title if title else None)

    st.plotly_chart(fig, use_container_width=True)

    if st.button("➕ Add to Dashboard", key="heatmap_add"):
        add_to_dashboard(fig, title or "Heatmap (Correlation)")
