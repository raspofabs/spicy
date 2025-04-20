"""Test the use-cases parser."""

import pytest

from spicy.md_read import parse_text_to_syntax_tree
from spicy.parser.use_case_constants import _get_usage_subsection, tcl_map


def test_spec_name_to_variant() -> None:
    """Test variants can be deduced from well formed spec names."""
    test_lines = [
        "- **Purpose:** to be.",
        "- **Inputs:** light, heat, food, drink, air.",
        "- **Outputs:** thoughts, wisdom, the occasional fart.",
        "- **Usage procedure:** observe its presence.",
        "- **Environmental constraints:** a type M planet.",
    ]

    test_text = "\n".join(test_lines)

    tree = parse_text_to_syntax_tree(test_text)
    assert tree.type == "root"
    bullet_list_node = tree.children[0]
    assert bullet_list_node.type == "bullet_list"

    # positive tests
    assert _get_usage_subsection(bullet_list_node, "Purpose:") == "to be."
    assert _get_usage_subsection(bullet_list_node, "usage procedure:") == "observe its presence."

    # negative tests
    assert _get_usage_subsection(bullet_list_node, "Why?") == ""
    with pytest.raises(TypeError, match="Node is wrong type: root"):
        assert _get_usage_subsection(tree, "Why?") == ""


def test_tcl_mappings() -> None:
    """Test the TCL mappings."""
    assert tcl_map(None, None) is not None
    assert tcl_map(None, None) == "<undefined>"
    with pytest.raises(ValueError, match="Invalid impact.*carrot"):
        tcl_map("carrot", None)
    with pytest.raises(ValueError, match="Invalid impact.*prune"):
        tcl_map("prune", "TD1")
    with pytest.raises(ValueError, match="Invalid detectability.*melon"):
        tcl_map(None, "melon")
    with pytest.raises(ValueError, match="Invalid detectability.*apple"):
        tcl_map("TI1", "apple")

    # impact 1
    assert tcl_map("TI1", "TD1") == "TCL1"
    assert tcl_map("TI1", "TD2") == "TCL1"
    assert tcl_map("TI1", "TD3") == "TCL1"

    # impact 2
    assert tcl_map("TI2", "TD1") == "TCL1"
    assert tcl_map("TI2", "TD2") == "TCL2"
    assert tcl_map("TI2", "TD3") == "TCL3"
