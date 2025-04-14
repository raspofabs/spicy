"""Test the use-cases parser."""

import logging
import pytest
from pathlib import Path

from spicy.gather import get_elements_from_files
from spicy.parser import SpecElement, SpecParser, parse_syntax_tree_to_spec_elements
from spicy.md_read import load_syntax_tree, parse_text_to_syntax_tree

def test_gather_on_directory(test_data_path) -> None:
    """Test we can gather from a directory, not just a single file."""
    spec_element_list = get_elements_from_files("TD", [test_data_path / "use_cases"])

    assert isinstance(spec_element_list, list)
    assert len(spec_element_list) > 1

