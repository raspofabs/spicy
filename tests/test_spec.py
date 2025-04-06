"""Test the spec parser."""

from pathlib import Path

import pytest

from spicy.spec import SpecElementBase, gather_spec_elements
from spicy.spec.builder import (
    SoftwareRequirement,
    StakeholderNeed,
    StakeholderRequirement,
    SystemElement,
    SystemRequirement,
)


def test_simple_spec(test_data_path: Path) -> None:
    """Test a very simple spec."""
    spec_list = gather_spec_elements("td", test_data_path / "spec" / "spec_sys1_stakeholder_requirements.md")
    assert isinstance(spec_list, list)
    assert len(spec_list) > 0
    spec_element = spec_list[0]
    assert issubclass(type(spec_element), SpecElementBase)

    assert spec_element.name == "TD_STK_NEED_get_a_cookie"


def test_complete_spec(test_data_path: Path) -> None:
    """Test a set of spec files."""
    spec_list = gather_spec_elements("td", test_data_path / "spec")
    assert isinstance(spec_list, list)
    assert len(spec_list) > 0

    first_spec_element = spec_list[0]
    assert issubclass(type(first_spec_element), SpecElementBase)

    assert all(issubclass(type(x), SpecElementBase) for x in spec_list)

    assert any(x.name == "TD_STK_NEED_get_a_cookie" for x in spec_list)


spec_parts_data = [
    ("TD_STK_NEED_get_a_cookie", StakeholderNeed),
    ("TD_STK_REQ_cookie_orders", StakeholderRequirement),
    ("TD_SYS_REQ_cookie_ordering", SystemRequirement),
    ("TD_SYS_ELEMENT_cookie_storage", SystemElement),
    ("TD_SW_REQ_cookie_order_persistence", SoftwareRequirement),
]


@pytest.mark.parametrize(("expected_name", "expected_class"), spec_parts_data)
def test_spec_parts(test_data_path: Path, expected_name: str, expected_class: type) -> None:
    """Test that spec parts are detected correctly."""
    spec_list = gather_spec_elements("td", test_data_path / "spec")

    spec_by_name = {x.name: x for x in spec_list}

    assert expected_name in spec_by_name
    assert isinstance(spec_by_name[expected_name], expected_class)
