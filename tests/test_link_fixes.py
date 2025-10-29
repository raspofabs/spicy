"""Test the link_fixes.py module."""

import re
from pathlib import Path

from spicy.link_fixes import get_section_pattern_from_prefix, get_targets_from_md


def test_get_section_pattern_from_prefix() -> None:
    """Test the section pattern matches sections based on the prefix."""
    expression = get_section_pattern_from_prefix("ABC")
    assert expression == re.compile(r"^#+ (ABC_\w+)$")
    m = expression.match("# ABC_123")
    assert m
    assert len(m.groups()) > 0
    assert m.group(1) == "ABC_123"


def test_get_targets_from_md(test_data_path: Path) -> None:
    """Test the get_targets_from_md function can get all valid refs."""
    content = test_data_path / "md_links" / "simple.md"
    found = get_targets_from_md(content.read_text(), get_section_pattern_from_prefix("PRE"))
    expected = [
        "PRE_first_heading",
        "PRE_second_heading",
    ]
    assert len(found) == len(expected)
    assert sorted(expected) == sorted(found)
    # check the line numbers are at least in the right order
    assert found["PRE_first_heading"] < found["PRE_second_heading"]
