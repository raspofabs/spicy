"""Test the use spec checker cli."""

import logging
import re
from pathlib import Path

import pytest
from click.testing import CliRunner

from spicy.entry_point import run


def test_single_file(test_data_path: Path) -> None:
    """Test accessing a single file."""
    runner = CliRunner()
    result = runner.invoke(
        run,
        ["--project-prefix", "TD", str(test_data_path / "spec" / "spec_sys1_stakeholder_needs.md")],
    )
    assert result.exit_code == 1, result.stdout

    result = runner.invoke(
        run,
        ["--project-prefix", "WRONG_PREFIX", str(test_data_path / "spec" / "spec_sys1_stakeholder_needs.md")],
    )
    assert result.exit_code == 1, result.stdout


def test_single_file_no_prefix(test_data_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test accessing a single file."""
    runner = CliRunner()
    with caplog.at_level(logging.DEBUG):
        result = runner.invoke(run, [str(test_data_path / "spec" / "spec_sys1_stakeholder_needs.md")])
    assert result.exit_code == 1, result.stdout
    assert "Unable to scan without a known prefix" in caplog.text


def test_simple_use_case_output(positive_test_data_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test the simple positive use case."""
    runner = CliRunner()
    runner.invoke(run, ["-v", str(positive_test_data_path)])

    # all logging
    assert "Found 1 files to read." in caplog.text
    assert re.search(r"Discovered \d+ elements.", caplog.text)


def test_simple_use_case_carefully(positive_test_data_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test the simple positive use case."""
    runner = CliRunner()
    with caplog.at_level(logging.INFO):
        result = runner.invoke(run, ["--project-prefix", "POS", str(positive_test_data_path)])
    assert result.exit_code == 0, result.stdout

    # no logging
    assert "Found 1 files to read." not in caplog.text
    assert "Discovered 11 spec elements." not in caplog.text

    # verify we don't need the prefix if we have a spicy.yaml
    with caplog.at_level(logging.INFO):
        result = runner.invoke(run, [str(positive_test_data_path)])
    assert result.exit_code == 0, result.stdout

    # no logging
    assert "Found 1 files to read." not in caplog.text
    assert "Discovered 11 spec elements." not in caplog.text

    with caplog.at_level(logging.DEBUG):
        result = runner.invoke(run, ["-v", str(positive_test_data_path)])
    assert result.exit_code == 0, result.stdout

    # all logging
    assert "Found 1 files to read." in caplog.text
    assert re.search(r"Discovered \d+ elements.", caplog.text)


@pytest.mark.xfail
def test_bad_link_case(bad_link_data_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test the simple bad-link spec."""
    runner = CliRunner()

    # checking without checking, it's okay.
    with caplog.at_level(logging.INFO):
        result = runner.invoke(run, [str(bad_link_data_path)])
    assert result.exit_code == 0, result.stdout

    # checking links, it's not okay.
    with caplog.at_level(logging.INFO):
        result = runner.invoke(run, [str(bad_link_data_path), "--check-refs"])
    assert result.exit_code != 0, result.stdout

    assert "[LINK ISSUE] Bad link in complete_spec.md" in caplog.text


def test_hierarcical_case(test_data_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test the hierarcical_case positive use case."""
    runner = CliRunner()
    with caplog.at_level(logging.DEBUG):
        result = runner.invoke(run, [str(test_data_path / "hierarchical_test_spec")])
    assert result.exit_code == 0, result.stdout

    # all logging
    assert "Found 1 files to read." not in caplog.text
    assert re.search(r"Discovered \d+ elements.", caplog.text)


def test_various_data(test_data_path: Path) -> None:
    """Test the general test data folder."""
    runner = CliRunner()

    # complete directory
    result = runner.invoke(run, ["-p", "TD", str(test_data_path / "spec")])
    assert result.exit_code == 1, result.stdout
    assert "StakeholderNeed without a StakeholderRequirement" in result.stdout

    # one file
    result = runner.invoke(run, ["-p", "TD", str(test_data_path / "spec" / "spec_swe1_software_requirements.md")])
    assert result.exit_code == 1, result.stdout
    line1 = r"SoftwareRequirement.*\n"
    line2 = r"Missing links for \[Realises SystemRequirement\]"
    assert re.search(line1 + line2, result.stdout, re.MULTILINE)


def test_missing_config(test_data_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test that we need a specified prefix if we don't have a spicy.yaml."""
    runner = CliRunner()

    # verify we need the prefix if we don't have the yaml
    result = runner.invoke(run, [str(test_data_path)])
    assert result.exit_code == 1, result.stdout
    assert "Unable to scan without a known prefix" in caplog.text
