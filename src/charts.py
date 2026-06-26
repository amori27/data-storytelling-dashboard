import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.config import CHART_COLORS


def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    title: str = "Bar Chart",
) -> go.Figure:
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        color_discrete_sequence=CHART_COLORS,
        barmode="group",
    )
    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        template="plotly_white",
        hovermode="x unified",
    )
    return fig


def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    title: str = "Line Chart",
) -> go.Figure:
    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        color_discrete_sequence=CHART_COLORS,
        markers=True,
    )
    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        template="plotly_white",
        hovermode="x unified",
    )
    return fig


def pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str = "Pie Chart",
) -> go.Figure:
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        color_discrete_sequence=CHART_COLORS,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(template="plotly_white")
    return fig


def scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    size: str | None = None,
    title: str = "Scatter Plot",
) -> go.Figure:
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        title=title,
        color_discrete_sequence=CHART_COLORS,
    )
    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        template="plotly_white",
    )
    return fig


def summary_table(df: pd.DataFrame) -> go.Figure:
    numeric_cols = df.select_dtypes(include="number").columns
    stats = df[numeric_cols].describe().T.reset_index()
    stats.columns = ["Column", "Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]
    for c in stats.columns[2:]:
        stats[c] = stats[c].round(2)

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(stats.columns),
                    fill_color="paleturquoise",
                    align="left",
                    font=dict(size=12),
                ),
                cells=dict(
                    values=[stats[c] for c in stats.columns],
                    align="left",
                    font=dict(size=11),
                ),
            )
        ]
    )
    fig.update_layout(title="Summary Statistics", height=400)
    return fig
