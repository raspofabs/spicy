"""Mapping functions for use cases."""


def tcl_map(impact: str, detectability: str):
    """Return the TCL given a TI and TD class."""
    assert impact in [None, "TI1", "TI2"]
    assert detectability in [None, "TD1", "TD2", "TD3"]
    if impact is None or detectability is None:
        return "<undefined>"
    if impact == "TI1":
        return "TCL1"
    return "TCL" + detectability[-1:]
