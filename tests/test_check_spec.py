"""Test the use spec checker cli."""

from pathlib import Path

from click.testing import CliRunner

from spicy.check_spec import run


def test_simple_use_case(positive_test_data_path: Path) -> None:
    """Test the simple positive use case."""
    runner = CliRunner()
    result = runner.invoke(run, ["POS", str(positive_test_data_path)])
    assert result.exit_code == 0, result.stdout


def test_complete_spec(test_data_path: Path) -> None:
    """Test the complete test spec data."""
    runner = CliRunner()
    result = runner.invoke(run, ["CDU", str(test_data_path)])
    assert result.exit_code == 1, result.stdout
    assert "Needs without a fulfilling stakeholder requirement" in result.stdout
