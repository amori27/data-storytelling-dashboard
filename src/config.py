from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DATA_PATH = DATA_DIR / "sample_sales.csv"

APP_TITLE = "Data Storytelling Dashboard"
APP_ICON = ":bar_chart:"

CHART_COLORS = [
    "#636EFA", "#EF553B", "#00CC96", "#AB63FA",
    "#FFA15A", "#19D3F3", "#FF6692", "#B6E880",
]

NUMBER_FORMAT = "{:,.2f}"

SUMMARY_STATS = ["mean", "median", "std", "min", "max"]
