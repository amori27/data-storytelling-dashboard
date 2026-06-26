# Data Storytelling Dashboard

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-1.35%2B-red)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/plotly-5.22%2B-green)](https://plotly.com)
[![Ruff](https://img.shields.io/badge/ruff-check-yellow)](https://docs.astral.sh/ruff)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

An interactive **data storytelling dashboard** built with Streamlit and Plotly. Upload a CSV or use the sample dataset to auto-generate bar, line, pie, and scatter charts with summary statistics. Export your dashboard as a self-contained HTML report.

## Features

- **CSV Ingestion** — Upload any CSV file or load the built-in sample sales dataset
- **Auto Column Detection** — Automatically identifies numeric, categorical, and date columns
- **4 Chart Types** — Bar, Line, Pie, and Scatter plots with interactive Plotly rendering
- **Summary Statistics** — Automatic descriptive statistics table for all numeric columns
- **HTML Export** — Export the full dashboard (charts + data preview) as a standalone HTML report
- **Clean UI** — Sidebar-driven controls with responsive layout

## Screenshots

<!-- Add screenshots here once you launch the app -->
| Dashboard View | Chart Configuration |
|---|---|
| ![Dashboard](https://via.placeholder.com/600x400?text=Dashboard+Preview) | ![Sidebar](https://via.placeholder.com/400x400?text=Sidebar+Controls) |

## Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd data-storytelling-dashboard

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run src/app.py
```

Then open your browser to `http://localhost:8501`.

## Step-by-Step Install Guide

### 1. Prerequisites

- Python 3.11 or later
- pip (Python package manager)

### 2. Set up a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate    # Linux / macOS
venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run src/app.py
```

### 5. (Optional) Run tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
data-storytelling-dashboard/
├── data/
│   └── sample_sales.csv          # Sample dataset (60 rows)
├── src/
│   ├── __init__.py
│   ├── app.py                   # Streamlit entry point
│   ├── loader.py                # CSV loading + validation
│   ├── charts.py                # Plotly chart generators
│   ├── reporter.py              # HTML report export
│   └── config.py                # App configuration
├── tests/
│   ├── __init__.py
│   ├── test_loader.py
│   ├── test_charts.py
│   └── test_reporter.py
├── .github/workflows/
│   └── ci-cd.yml               # CI pipeline (ruff + pytest)
├── requirements.txt
├── LICENSE
└── README.md
```

## Usage

1. **Choose data source** — Select "Upload CSV" to load your own file, or "Sample Dataset" to use the built-in sales data
2. **Configure charts** — Pick chart type, X/Y axes, and optional color/size grouping from the sidebar
3. **Explore** — View the interactive chart and summary statistics on the main panel
4. **Export** — Click "Export HTML Report" in the sidebar to save a standalone report

## Development

### Linting

```bash
ruff check src/ tests/
```

### Testing

```bash
python -m pytest tests/ -v --cov=src
```

## License

[MIT](LICENSE)
