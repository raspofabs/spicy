"""Test the use-cases parser."""

from pathlib import Path

from spicy.gather import gather_all_elements, get_elements_from_files


def test_gather_all_elements(test_data_path: Path) -> None:
    """Test we can render some issues with obvious errors."""
    spec_elements = gather_all_elements("TD", test_data_path / "simple" / "duped.md")

    assert isinstance(spec_elements, list)
    assert len(spec_elements) > 1


def test_gather_on_directory(test_data_path: Path) -> None:
    """Test we can gather from a directory, not just a single file."""
    spec_element_list = get_elements_from_files("TD", [test_data_path / "use_cases"])

    assert isinstance(spec_element_list, list)
    assert len(spec_element_list) > 1
