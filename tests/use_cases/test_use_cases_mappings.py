"""Test the use-cases parser."""

import pytest

from spicy.use_cases.mappings import tcl_map


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
