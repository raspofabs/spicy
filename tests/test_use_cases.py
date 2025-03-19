"""Test the use-cases parser."""

from pathlib import Path

from spicy.use_cases import UseCase, gather_use_cases


def test_valid_use_case(test_data_path: Path) -> None:
    """Positive test the tooling using good data."""
    use_case_list = gather_use_cases(test_data_path / "use_cases" / "01_simple_valid.md")
    assert isinstance(use_case_list, list)
    assert len(use_case_list) > 0
    use_case = next(case for case in use_case_list if case.name == "FEAT_COOKIE_ORDERING_PAGE")
    assert isinstance(use_case, UseCase)

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


def test_invalid_use_case(test_data_path: Path) -> None:
    """Negative test the tooling using the invalid data."""
    use_case_list = gather_use_cases(test_data_path / "use_cases" / "02_mostly_invalid.md")
    assert isinstance(use_case_list, list)
    assert len(use_case_list) > 0
    use_case = next(case for case in use_case_list if case.name == "FEAT_INVALID")
    assert isinstance(use_case, UseCase)

    assert use_case.name == "FEAT_INVALID"
    assert not use_case.description_text()
    assert not use_case.features_text()
    assert not use_case.inputs()
    assert not use_case.outputs()
    assert not use_case.impact_rationale()
    assert not use_case.detectability_rationale()

    assert use_case.impact is None
    assert use_case.detectability is None
    assert use_case.tcl == "<undefined>"

    issues = use_case.get_issues()
    assert issues

    # fragile tests
    assert f"Issues in {use_case.file_path.name}, {use_case.name}" in issues
    assert "no impact" in issues
    assert "no detectability" in issues
    assert "5 no usage: inputs,outputs,purpose,usage,environment" in issues
    assert "4 no section information for :prologue,features,tool_impact,detectability" in issues


def test_high_tcl(test_data_path: Path) -> None:
    """Test the high tcl rating test data."""
    use_case_list = gather_use_cases(test_data_path / "use_cases" / "04_high_tcl.md")
    assert isinstance(use_case_list, list)
    assert len(use_case_list) > 0
    use_case = next(case for case in use_case_list if case.name == "FEAT_HOT_OVEN")
    assert isinstance(use_case, UseCase)

    assert use_case.name == "FEAT_HOT_OVEN"
    assert use_case.impact == "TI2"
    assert use_case.detectability == "TD2"
    assert use_case.tcl == "TCL2"
    assert use_case.safety_case == True
