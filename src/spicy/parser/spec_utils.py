"""Spec specific constants and utility functions."""

from functools import lru_cache


def spec_name_to_variant(name: str) -> str | None:
    """Return the variant by guessing from the name, or give up and return None."""
    parts = name.split("_")
    minimum_parts = 3
    if len(parts) < minimum_parts:
        return None
    _project_prefix, *variant_parts = parts
    comparison_string = "_".join(variant_parts)

    guesses = []
    for variant_string, variant in {
        "STK_NEED": "StakeholderNeed",
        "STK_REQ": "StakeholderRequirement",
        "SYS_REQ": "SystemRequirement",
        "SYS_ELEMENT": "SystemElement",
        "SW_REQ": "SoftwareRequirement",
        "SW_ARCH": "SoftwareArchitecture",
        "SW_UNIT": "SoftwareUnit",
        "SW_UNIT_TEST": "SoftwareUnitTest",
        "SW_UNIT_INT": "SoftwareUnitIntegration",
        "SW_COMP": "SoftwareComponent",
        "SW_COMP_TEST": "SoftwareComponentTest",
        "SW_INT": "SoftwareIntegration",
        "SW_QUAL": "SoftwareQualification",
        "SYS_INT": "SystemIntegration",
        "SYS_QUAL": "SystemQualification",
        "VAL": "Validation",
    }.items():
        if comparison_string.startswith(variant_string):
            try:
                __, post = comparison_string.split(variant_string)
            except ValueError:
                return None
            if post and post[0] not in " _-":
                return None
            guesses.append(variant)
    if guesses:
        return sorted(guesses, reverse=True, key=lambda x: len(x))[0]
    return None


MappingType = dict[str, list[tuple[str, str]]]

_spec_is_software: set[str] = {
    "SoftwareRequirement",
    "SoftwareArchitecture",
    "SoftwareComponent",
    "SoftwareUnit",
    "SoftwareUnitTest",
    "SoftwareUnitIntegration",
    "SoftwareComponentTest",
    "SoftwareIntegration",
    "SoftwareQualification",
}

_spec_link_mapping: MappingType = {
    "StakeholderRequirement": [("Implements", "StakeholderNeed")],
    "SystemRequirement": [("Derived from", "StakeholderRequirement")],
    "SystemElement": [("Implements", "SystemRequirement")],
    "SystemIntegration": [("Integrates", "SystemElement")],
    "SystemQualification": [("Tests", "SystemRequirement")],
    "Validation": [("Tests", "StakeholderRequirement")],
    "SoftwareRequirement": [("Realises", "SystemRequirement"), ("Decomposes", "SystemElement")],
    "SoftwareArchitecture": [("Fulfils", "SoftwareRequirement")],
    "SoftwareComponent": [("Implements", "SoftwareArchitecture"), ("Fulfils", "SoftwareRequirement")],
    "SoftwareUnit": [("Implements", "SoftwareComponent")],
    "SoftwareUnitTest": [("Tests", "SoftwareUnit")],
    "SoftwareUnitIntegration": [("Integrates", "SoftwareUnit")],
    "SoftwareComponentTest": [("Tests", "SoftwareComponent")],
    "SoftwareIntegration": [("Integrates", "SoftwareComponent")],
    "SoftwareQualification": [("Tests", "SoftwareRequirement")],
    "UseCase": [("Fulfils", "StakeholderNeed")],
}

_spec_link_optional_mapping: MappingType = {
    "StakeholderNeed": [("Fulfilled by", "StakeholderRequirement"), ("Qualified as", "UseCase")],
    "StakeholderRequirement": [
        ("Derives to", "SystemRequirement"),
        ("Implemented by", "SystemElement"),
        ("Validated by", "Validation"),
    ],
    "SystemRequirement": [
        ("Implemented as", "SystemElement"),
        ("Tested by", "SystemQualification"),
        ("Requires", "SoftwareRequirement"),
    ],
    "SystemElement": [("Composes", "SoftwareRequirement"), ("Integrated by", "SystemIntegration")],
    "SoftwareRequirement": [("Fulfilled by", "SoftwareArchitecture"), ("Tested by", "SoftwareQualification")],
    "SoftwareArchitecture": [("Implemented by", "SoftwareComponent")],
    "SoftwareComponent": [
        ("Implemented by", "SoftwareUnit"),
        ("Integrated by", "SoftwareIntegration"),
        ("Tested by", "SoftwareComponentTest"),
    ],
    "SoftwareUnit": [("Integrated by", "SoftwareUnitIntegration"), ("Tested by", "SoftwareUnitTest")],
}


@lru_cache
def expected_links_for_variant(
    variant: str,
    *,
    include_optional: bool = False,
    non_functional: bool = False,
) -> list[tuple[str, str]]:
    """Return a list of (link-name, target-variant) tuples.

    These are the links that should be present in the spec.
    For example, any testing specs should have links to what requirement they
    test.
    Lacking regular links implies the spec is in draft: unfinished and
    incomplete.
    """
    extra: list[tuple[str, str]] = _spec_link_optional_mapping.get(variant, []) if include_optional else []
    # non_functional requirements don't have main links, only backlinks
    if non_functional:
        return extra
    return _spec_link_mapping.get(variant, []) + extra


@lru_cache
def expected_backlinks_for_variant(variant: str, *, include_optional: bool = False) -> list[tuple[str, str]]:
    """Return a list of (source-variant, link-name) tuples.

    These are the links that should be present in other specs for this spec.
    For example, any spec which needs testing should have a test spec linking
    to this one.
    Lacking the required backlinks usually means that the spec has not been
    refined or tested.
    """
    regular = [
        (source_spec, link)
        for source_spec, links in _spec_link_mapping.items()
        for link, destination_spec in links
        if destination_spec == variant
    ]
    extra = [
        (source_spec, link)
        for source_spec, links in _spec_link_optional_mapping.items()
        for link, destination_spec in links
        if destination_spec == variant
    ]
    if include_optional:
        return regular + extra
    return regular


@lru_cache
def _get_section_mapping() -> dict[str, str]:
    mapping = {
        "Safety related": "qualification_related",
        "Qualification related": "qualification_related",
        "Qualification relevant": "qualification_related",
        "TQP relevant": "qualification_related",
        "TCL relevant": "qualification_related",
        "Derived from": "derived_from",
        "Fulfils": "fulfils",
        "Fulfilled by": "fulfilled_by",
        "Software element": "software_requirement",
        "Implies software": "software_requirement",
        "Non functional": "non_functional_requirement",
        "Non-functional": "non_functional_requirement",
        "Implements": "implements",
        "Implemented by": "implemented_by",
        "Realises": "realises",
        "Tests": "tests",
        "Tested by": "tested_by",
        "Results": "results",
        "Cases": "cases",
        "verification criteria": "verification_criteria",
    }
    return {k.lower(): v for k, v in mapping.items()}


def section_name_to_key(section_name: str) -> str | None:
    """Return a proper key for the section name or None."""
    return _get_section_mapping().get(section_name.lower())


@lru_cache
def expected_variants() -> list[str]:
    """Return the set of all expected variants."""
    return sorted(set(_spec_link_mapping).union(set(_spec_link_optional_mapping)))


@lru_cache
def spec_is_defined(spec_type_name: str) -> bool:
    """Return whether a spec type is part of the defined set of spec types."""
    return spec_type_name in expected_variants()


@lru_cache
def spec_is_software(spec_type_name: str) -> bool:
    """Return whether a spec type is part of a software solution."""
    return spec_type_name in _spec_is_software
