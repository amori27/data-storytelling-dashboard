from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

from src.reporter import export_html_report, generate_html_report


def sample_figure(title: str = "Chart") -> tuple[str, str]:
    fig = go.Figure(data=[go.Scatter(x=[1, 2], y=[3, 4])])
    fig.update_layout(title=title)
    div = pio.to_html(fig, full_html=False, include_plotlyjs=False)
    return title, div


class TestGenerateHtmlReport:
    def test_contains_title(self) -> None:
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        html = generate_html_report(df, [sample_figure()])
        assert "Data Storytelling Dashboard" in html
        assert "Chart" in html

    def test_contains_data_preview(self) -> None:
        df = pd.DataFrame({"x": [10, 20], "y": [30, 40]})
        html = generate_html_report(df, [])
        assert "Data Preview" in html
        assert "10" in html

    def test_custom_stats(self) -> None:
        df = pd.DataFrame({"a": [1]})
        html = generate_html_report(df, [], stats_html="<div>Custom Stats</div>")
        assert "Custom Stats" in html

    def test_multiple_charts(self) -> None:
        df = pd.DataFrame({"a": [1]})
        html = generate_html_report(df, [sample_figure("A"), sample_figure("B")])
        assert html.count("<h2>") == 3


class TestExportHtmlReport:
    def test_export_creates_file(self, tmp_path: Path) -> None:
        output = tmp_path / "report.html"
        result = export_html_report("<html></html>", output)
        assert result == output.absolute()
        assert output.exists()
        assert output.read_text() == "<html></html>"
