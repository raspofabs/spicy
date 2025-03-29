"""Test the use spec checker cli."""

import re
from pathlib import Path

from click.testing import CliRunner

from spicy.check_spec import run


def test_simple_use_case(positive_test_data_path: Path) -> None:
    """Test the simple positive use case."""
    runner = CliRunner()
    result = runner.invoke(run, ["--project-prefix", "POS", str(positive_test_data_path)])
    assert result.exit_code == 0, result.stdout

    # verify we don't need it if we have a spicy.yaml
    result = runner.invoke(run, [str(positive_test_data_path)])
    assert result.exit_code == 0, result.stdout


def test_larger_spec(cookie_data_path: Path) -> None:
    """Test the complete test spec data."""
    runner = CliRunner()
    result = runner.invoke(run, ["--project-prefix", "CDU", str(cookie_data_path)])
    assert result.exit_code == 1, result.stdout
    assert "Needs without a fulfilling stakeholder requirement" in result.stdout

    result = runner.invoke(run, [str(cookie_data_path)])
    assert result.exit_code == 1, result.stdout
    assert "Needs without a fulfilling stakeholder requirement" in result.stdout


def test_various_data(test_data_path: Path) -> None:
    """Test the general test data folder."""
    runner = CliRunner()

    # complete directory
    result = runner.invoke(run, ["-p", "TD", str(test_data_path)])
    assert result.exit_code == 1, result.stdout
    assert "Needs without a fulfilling stakeholder requirement" in result.stdout

    # one file
    result = runner.invoke(run, ["-p", "TD", str(test_data_path / "spec" / "spec_swe1_software_requirements.md")])
    assert result.exit_code == 1, result.stdout
    assert re.search(r"SoftwareRequirement.*\n.*Does not fulfil any system requirement", result.stdout, re.MULTILINE)


def test_missing_config(test_data_path: Path, caplog) -> None:
    """Test that we need a specified prefix if we don't have a spicy.yaml."""
    runner = CliRunner()

    # verify we need the prefix if we don't have the yaml
    result = runner.invoke(run, [str(test_data_path)])
    assert result.exit_code == 1, result.stdout
    assert "Unable to scan without a known prefix" in caplog.text
