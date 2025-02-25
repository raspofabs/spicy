from spicy.use_cases import UseCase, gather_use_cases


def test_valid_use_case(test_data_path):
    use_case_list = gather_use_cases(test_data_path / "use_cases" / "01_simple_valid.md")
    assert isinstance(use_case_list, list)
    assert len(use_case_list) > 0
    use_case = use_case_list[0]
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

    issue_lines = []

    def writer(line):
        issue_lines.append(line)

    use_case.render_issues(writer)
    assert not issue_lines


def test_invalid_use_case(test_data_path):
    use_case_list = gather_use_cases(test_data_path / "use_cases" / "02_mostly_invalid.md")
    assert isinstance(use_case_list, list)
    assert len(use_case_list) > 0
    use_case = use_case_list[0]
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

    issue_lines = []

    def writer(line):
        issue_lines.append(line)

    use_case.render_issues(writer)
    assert issue_lines

    # fragile tests
    assert f"Issues in {use_case.file_path.name}, {use_case.name}" in issue_lines
    assert "\tno impact" in issue_lines
    assert "\tno detectability" in issue_lines
    assert "\t5 no usage: inputs,outputs,purpose,usage,environment" in issue_lines
    assert "\t4 no section information for :prologue,features,tool_impact,detectability" in issue_lines
