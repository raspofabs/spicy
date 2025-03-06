import pytest
from spicy.spec import SpecElement, gather_spec_elements
from spicy.spec.builder import (
    SoftwareRequirement,
    StakeholderNeed,
    StakeholderRequirement,
    SystemElement,
    SystemRequirement,
)


def test_simple_spec(test_data_path):
    """Test a very simple spec."""
    spec_list = gather_spec_elements("cdu", test_data_path / "spec" / "spec_sys1_stakeholder_requirements.md")
    assert isinstance(spec_list, list)
    assert len(spec_list) > 0
    spec_element = spec_list[0]
    assert issubclass(type(spec_element), SpecElement)

    assert spec_element.name == "CDU_STK_NEED_get_a_cookie"


def test_complete_spec(test_data_path):
    """Test a set of spec files."""
    spec_list = gather_spec_elements("cdu", test_data_path / "spec")
    assert isinstance(spec_list, list)
    assert len(spec_list) > 0

    first_spec_element = spec_list[0]
    assert issubclass(type(first_spec_element), SpecElement)

    assert all(issubclass(type(x), SpecElement) for x in spec_list)

    assert any(x.name == "CDU_STK_NEED_get_a_cookie" for x in spec_list)


spec_parts_data = [
    ("CDU_STK_NEED_get_a_cookie", StakeholderNeed),
    ("CDU_STK_REQ_cookie_orders", StakeholderRequirement),
    ("CDU_SYS_REQ_cookie_ordering", SystemRequirement),
    ("CDU_SYS_ELEMENT_cookie_storage", SystemElement),
    ("CDU_SW_REQ_cookie_order_persistence", SoftwareRequirement),
]


@pytest.mark.parametrize("expected_name, expected_class", spec_parts_data)
def test_spec_parts(test_data_path, expected_name, expected_class):
    """Test that spec parts are detected correctly."""
    spec_list = gather_spec_elements("cdu", test_data_path / "spec")

    spec_by_name = {x.name: x for x in spec_list}

    assert expected_name in spec_by_name
    assert isinstance(spec_by_name[expected_name], expected_class)
