import pandas as pd
import plotly.graph_objects as go
import pytest

from src.charts import bar_chart, line_chart, pie_chart, scatter_chart, summary_table


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({
        "category": ["A", "B", "C", "A", "B", "C"],
        "values": [10, 20, 30, 15, 25, 35],
        "group": ["X", "X", "Y", "Y", "Z", "Z"],
    })


class TestBarChart:
    def test_returns_figure(self, sample_df: pd.DataFrame) -> None:
        fig = bar_chart(sample_df, x="category", y="values")
        assert isinstance(fig, go.Figure)

    def test_with_color(self, sample_df: pd.DataFrame) -> None:
        fig = bar_chart(sample_df, x="category", y="values", color="group")
        assert len(fig.data) > 0

    def test_title(self, sample_df: pd.DataFrame) -> None:
        fig = bar_chart(sample_df, x="category", y="values", title="Test Bar")
        assert fig.layout.title.text == "Test Bar"


class TestLineChart:
    def test_returns_figure(self, sample_df: pd.DataFrame) -> None:
        fig = line_chart(sample_df, x="category", y="values")
        assert isinstance(fig, go.Figure)

    def test_markers_enabled(self, sample_df: pd.DataFrame) -> None:
        fig = line_chart(sample_df, x="category", y="values")
        assert fig.data[0].mode == "lines+markers"


class TestPieChart:
    def test_returns_figure(self, sample_df: pd.DataFrame) -> None:
        fig = pie_chart(sample_df, names="category", values="values")
        assert isinstance(fig, go.Figure)

    def test_labels(self, sample_df: pd.DataFrame) -> None:
        fig = pie_chart(sample_df, names="category", values="values")
        assert set(fig.data[0].labels) == {"A", "B", "C"}


class TestScatterChart:
    def test_returns_figure(self, sample_df: pd.DataFrame) -> None:
        fig = scatter_chart(sample_df, x="category", y="values")
        assert isinstance(fig, go.Figure)

    def test_with_color_and_size(self, sample_df: pd.DataFrame) -> None:
        fig = scatter_chart(sample_df, x="category", y="values", color="group", size="values")
        assert len(fig.data) > 0


class TestSummaryTable:
    def test_returns_figure(self, sample_df: pd.DataFrame) -> None:
        fig = summary_table(sample_df)
        assert isinstance(fig, go.Figure)
