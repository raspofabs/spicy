"""Test the use-cases parser."""

import pytest

from spicy.gather import get_elements_from_files
from spicy.md_read import load_syntax_tree, parse_text_to_syntax_tree
from spicy.parser import SpecElement, SpecParser, parse_syntax_tree_to_spec_elements


def test_gather_on_directory(test_data_path) -> None:
    """Test we can gather from a directory, not just a single file."""
    spec_element_list = get_elements_from_files("TD", [test_data_path / "use_cases"])

    assert isinstance(spec_element_list, list)
    assert len(spec_element_list) > 1
