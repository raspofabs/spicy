import pytest
from spicy.spec import SpecElement, gather_spec_elements
from spicy.spec.builder import StakeholderNeed, StakeholderRequirement, SystemRequirement


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


spec_parts_data = [
    ("CDU_STK_NEED_1_get_a_cookie", StakeholderNeed),
    ("CDU_STK_REQ_1_cookie_orders", StakeholderRequirement),
    ("CDU_SYS_REQ_1_1_cookie_ordering", SystemRequirement),
]


@pytest.mark.parametrize("expected_name, expected_class", spec_parts_data)
def test_spec_parts(test_data_path, expected_name, expected_class):
    spec_list = gather_spec_elements("cdu", test_data_path / "spec")

    spec_by_name = {x.name: x for x in spec_list}

    assert expected_name in spec_by_name
    assert isinstance(spec_by_name[expected_name], expected_class)
