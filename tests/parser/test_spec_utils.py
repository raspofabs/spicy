"""Test the use-cases parser."""


from spicy.parser.spec_utils import (
    expected_backlinks_for_variant,
    expected_links_for_variant,
    section_name_to_key,
    spec_is_defined,
    spec_is_software,
    spec_name_to_variant,
)


def test_spec_name_to_variant() -> None:
    """Test variants can be deduced from well formed spec names."""
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
    """Test we can get the list of required and optional links for a spec."""
    assert expected_links_for_variant("SystemRequirement") == [("Derived from", "StakeholderRequirement")]

    # expect more if you include optional links (usually bi-directional backlinks)
    assert expected_links_for_variant("StakeholderRequirement", include_optional=False) == [
        ("Implements", "StakeholderNeed"),
    ]
    assert expected_links_for_variant("StakeholderRequirement", include_optional=True) == [
        ("Implements", "StakeholderNeed"),
        ("Derives to", "SystemRequirement"),
        ("Implemented by", "SystemElement"),
        ("Validated by", "Validation"),
    ]

    assert expected_backlinks_for_variant("StakeholderNeed") == [
        ("StakeholderRequirement", "Implements"),
        ("UseCase", "Fulfils"),
    ]
    assert expected_backlinks_for_variant("StakeholderNeed", include_optional=True) == [
        ("StakeholderRequirement", "Implements"),
        ("UseCase", "Fulfils"),
    ]


def test_section_name_to_key() -> None:
    """Test section_name_to_key function produces the right keys."""
    # test for the qualification related headings
    assert section_name_to_key("Safety related") == "qualification_related"
    assert section_name_to_key("Qualification related") == "qualification_related"
    assert section_name_to_key("Qualification relevant") == "qualification_related"
    assert section_name_to_key("TQP relevant") == "qualification_related"
    assert section_name_to_key("TCL relevant") == "qualification_related"

    # other section names
    assert section_name_to_key("Fulfils") == "fulfils"
    assert section_name_to_key("Implemented by") == "implemented_by"

    # test a negative with something random
    assert section_name_to_key("Boiled carrots") is None


def test_spec_is_defined() -> None:
    """Test the spec_is_defined function works, returning True iff the spec is valid."""
    assert spec_is_defined("SystemRequirement")
    assert not spec_is_defined("SystemRequirements")
    assert spec_is_defined("UseCase")
    assert spec_is_defined("StakeholderNeed")
    assert spec_is_defined("SoftwareRequirement")
    assert spec_is_defined("SystemElement")
    assert not spec_is_defined("SoftwareElement")
    assert not spec_is_defined("")


def test_spec_software_requirement_trait() -> None:
    """Test the general spec trait of software relevance."""
    assert spec_is_software("SoftwareRequirement")
    assert spec_is_software("SoftwareQualification")
    assert not spec_is_software("SystemRequirement")
    assert not spec_is_software("SystemElement")
