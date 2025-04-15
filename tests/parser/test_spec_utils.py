"""Test the use-cases parser."""

import logging
import pytest
from pathlib import Path

from spicy.gather import get_elements_from_files
from spicy.parser import SpecElement, SpecParser, parse_syntax_tree_to_spec_elements
from spicy.parser.spec_utils import spec_name_to_variant, expected_links_for_variant, expected_backlinks_for_variant, section_name_to_key

def test_spec_name_to_variant() -> None:
    assert spec_name_to_variant("Not a spec name") is None
    assert spec_name_to_variant("PRJPREF_NOT_A_SPEC") is None
    assert spec_name_to_variant("PRJPREF_STK_REQ") == "StakeholderRequirement"
    assert spec_name_to_variant("PRJ_STK_NEED") == "StakeholderNeed"
    assert spec_name_to_variant("ABC_SYS_REQ") == "SystemRequirement"
    assert spec_name_to_variant("123_SW_REQ_happiness") == "SoftwareRequirement"
    assert spec_name_to_variant("NE_SW_ARCH_cattle_grid") == "SoftwareArchitecture"
    assert spec_name_to_variant("NE_SW_ARCHES_dumbo") != "SoftwareArchitecture"
    assert spec_name_to_variant("ABC_SYS_REQ_SYS_REQ_Multi") is None


def test_expected_links_for_variant() -> None:
    assert expected_links_for_variant("SystemRequirement") == [("Derived from", "StakeholderRequirement")]

    # expect more if you include optional links (usually bi-directional backlinks)
    assert expected_links_for_variant("StakeholderRequirement", False) == [("Fulfils", "StakeholderNeed")]
    assert expected_links_for_variant("StakeholderRequirement", True) == [("Fulfils", "StakeholderNeed"), ("Derives to", "SystemRequirement"), ("Validated by", "Validation")]

    assert expected_backlinks_for_variant("StakeholderNeed") == [("StakeholderRequirement", "Fulfils"), ("UseCase", "Fulfils")]
    assert expected_backlinks_for_variant("StakeholderNeed", True) == [("StakeholderRequirement", "Fulfils"), ("UseCase", "Fulfils")]


def test_section_name_to_key() -> None:
    assert section_name_to_key("Safety related") == "qualification_related"
