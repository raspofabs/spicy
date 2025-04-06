"""Test the use-cases parser."""

from pathlib import Path

from spicy.spec import get_elements_from_files


def test_valid_use_case(test_data_path: Path) -> None:
    """Positive test the tooling using good data."""
    spec_element_list = get_elements_from_files("CDU", [test_data_path / "use_cases" / "01_simple_valid.md"])

    assert isinstance(spec_element_list, list)
    assert len(spec_element_list) == 1

    use_case = spec_element_list[0]

    assert use_case.name == "FEAT_COOKIE_ORDERING_PAGE"
    assert use_case.description_text()
    assert use_case.features_text()
    assert use_case.inputs()
    assert use_case.outputs()
    assert use_case.impact_rationale()
    assert use_case.detectability_rationale()

    assert use_case.impact == "TI2"
    assert use_case.detectability == "TD1"
    assert use_case.tcl == "TCL1"

    issues = use_case.get_issues()
    assert not issues
