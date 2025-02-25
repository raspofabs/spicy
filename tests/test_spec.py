from spicy.spec import SpecElement, gather_spec_elements


def test_simple_spec(test_data_path):
    spec_list = gather_spec_elements("cdu", test_data_path / "spec" / "spec_sys1_stakeholder_requirements.md")
    assert isinstance(spec_list, list)
    assert len(spec_list) > 0
    spec_element = spec_list[0]
    assert isinstance(spec_element, SpecElement)

    assert spec_element.name == "CDU_STK_NEED_1_get_a_cookie"


def test_complete_spec(test_data_path):
    spec_list = gather_spec_elements("cdu", test_data_path / "spec")
    assert isinstance(spec_list, list)
    assert len(spec_list) > 0
    spec_element = spec_list[0]
    assert isinstance(spec_element, SpecElement)

    assert spec_element.name == "CDU_STK_NEED_1_get_a_cookie"
