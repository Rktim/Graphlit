import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from modules.insights import overview_panel
from modules.visualization import (
    bar_chart, line_chart, scatter_chart, pie_chart,
    histogram, box_plot, heatmap
)
from modules.utils import uid

# Color presets
PALETTES = {
    # Sequential (good for continuous data)
    "Viridis": px.colors.sequential.Viridis,
    "Cividis": px.colors.sequential.Cividis,
    "Plasma": px.colors.sequential.Plasma,
    "Magma": px.colors.sequential.Magma,
    "Inferno": px.colors.sequential.Inferno,
    "Turbo": px.colors.sequential.Turbo,
    "Aggrnyl": px.colors.sequential.Aggrnyl,
    "Sunset": px.colors.sequential.Sunset,
    "Teal": px.colors.sequential.Teal,
    "Gray": px.colors.sequential.Greys,

    # Qualitative (good for categories)
    "Plotly": px.colors.qualitative.Plotly,
    "Pastel": px.colors.qualitative.Pastel,
    "Set1": px.colors.qualitative.Set1,
    "Set2": px.colors.qualitative.Set2,
    "Set3": px.colors.qualitative.Set3,
    "Bold": px.colors.qualitative.Bold,
    "D3": px.colors.qualitative.D3,
    "Prism": px.colors.qualitative.Prism,
    "Safe": px.colors.qualitative.Safe,
    "Vivid": px.colors.qualitative.Vivid,
    "Dark2": px.colors.qualitative.Dark2,
    "Antique": px.colors.qualitative.Antique,

    # Diverging (good for highlighting deviations)
    "Spectral": px.colors.diverging.Spectral,
    "RdBu": px.colors.diverging.RdBu,
    "RdYlBu": px.colors.diverging.RdYlBu,
    "RdYlGn": px.colors.diverging.RdYlGn,
    "BrBG": px.colors.diverging.BrBG,
    "PiYG": px.colors.diverging.PiYG,
    "PuOr": px.colors.diverging.PuOr,
    "Earth": px.colors.diverging.Earth
}


def render_main():
    # Ensure dashboard exists
    if "dashboard" not in st.session_state:
        st.session_state.dashboard = []

    df = st.session_state.df_clean
    st.title("Smart Visual Analysis")

    if df is None:
        st.info("Load data from the sidebar to begin.")
        return

    # Tabs for cleaner navigation
    tab1, tab2, tab3 = st.tabs(["📈 Create Charts", "📊 Dashboard", "🔍 Insights"])

    # ======== TAB 1: Create Charts ========
    with tab1:
        left, right = st.columns([2, 3], gap="large")
        with left:
            viz_type = st.selectbox("Chart type", ["Bar", "Line", "Scatter", "Pie", "Histogram", "Box", "Heatmap"])
            preset = st.selectbox("Preset", ["Dashboard", "Publication", "Presentation"])
            palette_name = st.selectbox("Color palette", list(PALETTES.keys()))
            palette = PALETTES[palette_name]
            title = st.text_input("Title", value="")
            showlegend = st.checkbox("Show legend", value=True)
            rotate_x = st.slider("Rotate X ticks", -90, 90, 0)
            dtick = st.number_input("X tick interval (0=auto)", min_value=0.0, value=0.0, step=1.0)
            yfmt = st.selectbox("Y format", ["Default", "Currency ($)", "Percent"])
            yfmt = {"Default": None, "Currency ($)": "$,.2f", "Percent": ".0%"}[yfmt]
            agg = st.selectbox("Aggregation", ["none", "mean", "median", "mode", "sum", "max", "min", "count"])
            group_by = None  # Can be extended later for grouped visuals

        with right:
            if viz_type == "Bar":
                bar_chart(df, preset, palette, title, rotate_x, dtick, yfmt, showlegend, agg, group_by)
            elif viz_type == "Line":
                line_chart(df, preset, palette, title, rotate_x, dtick, yfmt, showlegend, agg, group_by)
            elif viz_type == "Scatter":
                scatter_chart(df, preset, palette, title, rotate_x, dtick, yfmt, showlegend, agg, group_by)
            elif viz_type == "Pie":
                pie_chart(df, preset, palette, title)
            elif viz_type == "Histogram":
                histogram(df, preset, palette, title, yfmt)
            elif viz_type == "Box":
                box_plot(df, preset, palette, title)
            elif viz_type == "Heatmap":
                heatmap(df, preset, palette, title)

    # ======== TAB 2: Dashboard ========
    with tab2:
        st.subheader("📊 Dashboard Canvas")
        dash = st.session_state.dashboard
        if not dash:
            st.info("No charts added yet — go to 'Create Charts' tab and click **➕ Add to Dashboard**.")
        else:
            cols = st.columns(2)
            to_remove = move_up = move_down = None
            for i, item in enumerate(list(dash)):
                col = cols[i % 2]
                with col:
                    st.subheader(f"{i+1}. {item.get('title', 'Chart')}")
                    if item.get("fig") is not None:
                        st.plotly_chart(item["fig"], use_container_width=True)
                    elif item.get("png_bytes"):
                        st.image(item["png_bytes"], use_container_width=True)
                    elif item.get("html"):
                        st.components.v1.html(item["html"], height=420)

                    # Action buttons for each chart
                    a, b, c = st.columns([1, 1, 1])
                    if a.button("↑", key=f"up_{item['id']}") and i > 0:
                        move_up = i
                    if b.button("↓", key=f"down_{item['id']}") and i < len(dash) - 1:
                        move_down = i
                    if c.button("Remove", key=f"rm_{item['id']}"):
                        to_remove = item

            # Reorder / Remove actions
            if to_remove:
                st.session_state.dashboard.remove(to_remove)
                st.experimental_rerun()
            if move_up is not None:
                dash[move_up - 1], dash[move_up] = dash[move_up], dash[move_up - 1]
                st.experimental_rerun()
            if move_down is not None:
                dash[move_down + 1], dash[move_down] = dash[move_down], dash[move_down + 1]
                st.experimental_rerun()

    # ======== TAB 3: Insights ========
    with tab3:
        overview_panel(df)
