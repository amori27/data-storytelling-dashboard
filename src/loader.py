from pathlib import Path

import pandas as pd


class DataLoadError(Exception):
    pass


def load_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise DataLoadError(f"File not found: {path}")
    if path.suffix.lower() != ".csv":
        raise DataLoadError(f"Invalid file type: {path.suffix}")
    try:
        df = pd.read_csv(path)
    except Exception as exc:
        raise DataLoadError(f"Failed to read CSV: {exc}") from exc
    if df.empty:
        raise DataLoadError("CSV file is empty")
    return df


def validate_dataframe(df: pd.DataFrame) -> list[str]:
    warnings: list[str] = []
    if df.isnull().any().any():
        cols_with_nulls = df.columns[df.isnull().any()].tolist()
        warnings.append(f"Missing values detected in columns: {', '.join(cols_with_nulls)}")
    if df.duplicated().any():
        warnings.append(f"Found {df.duplicated().sum()} duplicate rows")
    return warnings


def detect_column_types(df: pd.DataFrame) -> dict[str, str]:
    types: dict[str, str] = {}
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            types[col] = "date"
        elif pd.api.types.is_numeric_dtype(df[col]):
            types[col] = "numeric"
        else:
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio < 0.5 and df[col].nunique() < 20:
                types[col] = "categorical"
            else:
                types[col] = "text"
    return types


def sample_dataset() -> pd.DataFrame:
    import random as _random

    dates = pd.date_range("2024-01-01", periods=60, freq="W").tolist()
    products = (["Widget A", "Widget B", "Gadget X", "Gadget Y", "Doohickey"] * 12)[:60]
    categories = (["Widgets", "Widgets", "Gadgets", "Gadgets", "Doohickeys"] * 12)[:60]
    regions = (["North", "South", "East", "West", "Central"] * 12)[:60]
    sales = [round(100 + (i * 12.5) + _random.uniform(-50, 50), 2) for i in range(60)]
    quantities = [int(_random.randint(1, 50)) for _ in range(60)]
    profits = [round(10 + (i * 2.5) + _random.uniform(-20, 20), 2) for i in range(60)]

    data = {
        "date": dates,
        "product": products,
        "category": categories,
        "region": regions,
        "sales": sales,
        "quantity": quantities,
        "profit": profits,
    }
    return pd.DataFrame(data)
