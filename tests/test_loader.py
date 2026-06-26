from pathlib import Path

import pandas as pd
import pytest

from src.loader import DataLoadError, detect_column_types, load_csv, sample_dataset, validate_dataframe


class TestLoadCSV:
    def test_load_valid_csv(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "test.csv"
        csv_path.write_text("a,b,c\n1,2,3\n4,5,6")
        df = load_csv(csv_path)
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (2, 3)

    def test_file_not_found(self) -> None:
        with pytest.raises(DataLoadError, match="File not found"):
            load_csv("/nonexistent/path.csv")

    def test_invalid_extension(self, tmp_path: Path) -> None:
        p = tmp_path / "data.txt"
        p.write_text("a,b\n1,2")
        with pytest.raises(DataLoadError, match="Invalid file type"):
            load_csv(p)

    def test_empty_file(self, tmp_path: Path) -> None:
        p = tmp_path / "empty.csv"
        p.write_text("")
        with pytest.raises(DataLoadError, match="Failed to read"):
            load_csv(p)


class TestValidateDataframe:
    def test_no_warnings(self) -> None:
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        assert validate_dataframe(df) == []

    def test_missing_values(self) -> None:
        df = pd.DataFrame({"a": [1, None], "b": [3, 4]})
        warnings = validate_dataframe(df)
        assert any("Missing values" in w for w in warnings)
        assert "a" in warnings[0]

    def test_duplicates(self) -> None:
        df = pd.DataFrame({"a": [1, 1], "b": [2, 2]})
        warnings = validate_dataframe(df)
        assert any("duplicate" in w for w in warnings)


class TestDetectColumnTypes:
    def test_numeric(self) -> None:
        df = pd.DataFrame({"x": [1.0, 2.5, 3.0]})
        types = detect_column_types(df)
        assert types["x"] == "numeric"

    def test_categorical(self) -> None:
        df = pd.DataFrame({"cat": ["A", "B", "A", "B", "A", "B"]})
        types = detect_column_types(df)
        assert types["cat"] == "categorical"

    def test_date(self) -> None:
        df = pd.DataFrame({"dt": pd.to_datetime(["2024-01-01", "2024-01-02"])})
        types = detect_column_types(df)
        assert types["dt"] == "date"

    def test_text(self) -> None:
        df = pd.DataFrame({"txt": ["foo", "bar", "baz", "qux", "quux", "corge"]})
        types = detect_column_types(df)
        assert types["txt"] == "text"


class TestSampleDataset:
    def test_shape(self) -> None:
        df = sample_dataset()
        assert len(df) == 60
        assert list(df.columns) == ["date", "product", "category", "region", "sales", "quantity", "profit"]

    def test_column_types(self) -> None:
        df = sample_dataset()
        types = detect_column_types(df)
        assert types["date"] == "date"
        assert types["sales"] == "numeric"
        assert types["quantity"] == "numeric"
        assert types["profit"] == "numeric"
        assert types["product"] == "categorical"
        assert types["category"] == "categorical"
        assert types["region"] == "categorical"
