"""Test the use case checker cli."""

from pathlib import Path

from click.testing import CliRunner

from spicy.check_use_cases import run


def test_simple_use_case(test_data_path: Path) -> None:
    """Test the simple positive use case."""
    runner = CliRunner()
    result = runner.invoke(run, [str(test_data_path / "use_cases" / "01_simple_valid.md")])
    assert result.exit_code == 0, result.stdout


def test_general_use_cases(test_data_path: Path, caplog) -> None:
    """Test the simple positive use case."""
    runner = CliRunner()
    result = runner.invoke(run, [str(test_data_path / "use_cases")])
    assert "02_mostly_invalid.md, FEAT_INVALID" in result.stdout
    assert result.exit_code == 1, result.stdout
