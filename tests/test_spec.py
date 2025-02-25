from spicy.spec import SpecElement, gather_spec_elements
from spicy.spec.spec_stakeholder_need import StakeholderNeed
from spicy.spec.spec_stakeholder_requirement import StakeholderRequirement


def test_simple_spec(test_data_path):
    spec_list = gather_spec_elements("cdu", test_data_path / "spec" / "spec_sys1_stakeholder_requirements.md")
    assert isinstance(spec_list, list)
    assert len(spec_list) > 0
    spec_element = spec_list[0]
    assert issubclass(type(spec_element), SpecElement)

    assert spec_element.name == "CDU_STK_NEED_1_get_a_cookie"


def test_complete_spec(test_data_path):
    spec_list = gather_spec_elements("cdu", test_data_path / "spec")
    assert isinstance(spec_list, list)
    assert len(spec_list) > 0

    first_spec_element = spec_list[0]
    assert issubclass(type(first_spec_element), SpecElement)

    assert all(map(lambda x: issubclass(type(x), SpecElement), spec_list))

    assert any(map(lambda x: x.name == "CDU_STK_NEED_1_get_a_cookie", spec_list))

    for spec in spec_list:
        if spec.name == "CDU_STK_NEED_1_get_a_cookie":
            assert isinstance(spec, StakeholderNeed)
        if spec.name == "CDU_STK_REQ_1_cookie_orders":
            assert isinstance(spec, StakeholderRequirement)
