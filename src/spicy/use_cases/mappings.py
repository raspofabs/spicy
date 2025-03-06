"""Mapping functions for use cases."""


def tcl_map(impact: str | None, detectability: str | None) -> str:
    """Return the TCL given a TI and TD class."""
    if impact not in [None, "TI1", "TI2"]:
        msg = f"Invalid impact value : {impact}"
        raise ValueError(msg)
    if detectability not in [None, "TD1", "TD2", "TD3"]:
        msg = f"Invalid detectability value : {detectability}"
        raise ValueError(msg)
    if impact is None or detectability is None:
        return "<undefined>"
    if impact == "TI1":
        return "TCL1"
    return "TCL" + detectability[-1:]
