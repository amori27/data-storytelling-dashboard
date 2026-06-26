from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.charts import bar_chart, line_chart, pie_chart, scatter_chart, summary_table
from src.config import APP_ICON, APP_TITLE, SAMPLE_DATA_PATH
from src.loader import (
    DataLoadError,
    detect_column_types,
    load_csv,
    sample_dataset,
    validate_dataframe,
)
from src.reporter import export_html_report, generate_html_report

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
st.title(f"{APP_ICON} {APP_TITLE}")


@st.cache_data
def cached_load(path: str | Path) -> pd.DataFrame:
    return load_csv(path)


@st.cache_data
def cached_sample() -> pd.DataFrame:
    return sample_dataset()


def render_sidebar() -> tuple[pd.DataFrame, str, str, str, str, str]:
    with st.sidebar:
        st.header("Data Source")
        source = st.radio("Choose data source", ["Upload CSV", "Sample Dataset"])
        df: pd.DataFrame | None = None

        if source == "Upload CSV":
            uploaded: UploadedFile | None = st.file_uploader(
                "Choose a CSV file", type="csv"
            )
            if uploaded is not None:
                try:
                    df = pd.read_csv(uploaded)
                except Exception as exc:
                    st.error(f"Error reading file: {exc}")
                    st.stop()
            else:
                st.info("Upload a CSV file to get started.")
                st.stop()
        else:
            try:
                if SAMPLE_DATA_PATH.exists():
                    df = cached_load(SAMPLE_DATA_PATH)
                else:
                    df = cached_sample()
                st.success(f"Loaded sample dataset ({len(df)} rows)")
            except DataLoadError as exc:
                st.error(str(exc))
                st.stop()

        if df is None:
            st.stop()

        warnings = validate_dataframe(df)
        for w in warnings:
            st.warning(w)

        col_types = detect_column_types(df)

        st.header("Chart Configuration")
        numeric_cols = [c for c, t in col_types.items() if t == "numeric"]
        all_cols = list(df.columns)

        chart_type = st.selectbox(
            "Chart Type",
            ["Bar", "Line", "Pie", "Scatter"],
        )

        x_axis = st.selectbox("X-axis", all_cols, index=0)
        y_axis = st.selectbox(
            "Y-axis (numeric)",
            numeric_cols if numeric_cols else all_cols,
            index=0,
        )
        color_by = st.selectbox("Color by (optional)", ["None"] + all_cols)
        color_by = None if color_by == "None" else color_by

        size_by = None
        if chart_type == "Scatter":
            size_by = st.selectbox("Size by (optional)", ["None"] + numeric_cols)
            size_by = None if size_by == "None" else size_by

        return df, chart_type, x_axis, y_axis, color_by, size_by


df, chart_type, x_axis, y_axis, color_by, size_by = render_sidebar()

st.subheader("Data Preview")
with st.expander("Click to expand", expanded=True):
    st.dataframe(df.head(10), use_container_width=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Rows", len(df))
col2.metric("Columns", len(df.columns))
col3.metric("Numeric Columns", len(df.select_dtypes(include="number").columns))
col4.metric("Missing Values", int(df.isnull().sum().sum()))

st.subheader("Summary Statistics")
st.plotly_chart(summary_table(df), use_container_width=True)

st.subheader(f"Chart: {chart_type}")

fig = None
if chart_type == "Bar":
    fig = bar_chart(df, x=x_axis, y=y_axis, color=color_by)
elif chart_type == "Line":
    fig = line_chart(df, x=x_axis, y=y_axis, color=color_by)
elif chart_type == "Pie":
    fig = pie_chart(df, names=x_axis, values=y_axis)
elif chart_type == "Scatter":
    fig = scatter_chart(df, x=x_axis, y=y_axis, color=color_by, size=size_by)

if fig:
    st.plotly_chart(fig, use_container_width=True)

with st.sidebar:
    st.header("Export")
    if st.button("Export HTML Report"):
        with st.spinner("Generating report..."):
            chart_figures = []
            for ct, x, y, c, s in [
                ("Bar", x_axis, y_axis, color_by, None),
                ("Line", x_axis, y_axis, color_by, None),
                ("Pie", x_axis, y_axis, color_by, None),
                ("Scatter", x_axis, y_axis, color_by, size_by),
            ]:
                f = None
                if ct == "Bar":
                    f = bar_chart(df, x=x, y=y, color=c)
                elif ct == "Line":
                    f = line_chart(df, x=x, y=y, color=c)
                elif ct == "Pie":
                    f = pie_chart(df, names=x, values=y)
                elif ct == "Scatter":
                    f = scatter_chart(df, x=x, y=y, color=c, size=s)
                if f:
                    div = f.to_html(full_html=False, include_plotlyjs=False)
                    chart_figures.append((f"{ct} Chart", div))
            html = generate_html_report(df, chart_figures)
            path = export_html_report(html)
            st.success(f"Report saved to `{path}`")
            with open(path, "rb") as fh:
                st.download_button(
                    "Download HTML Report",
                    data=fh,
                    file_name="dashboard_report.html",
                    mime="text/html",
                )
