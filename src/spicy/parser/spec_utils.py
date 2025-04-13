"""Spec specific constants and utility functions."""

from functools import lru_cache

def spec_name_to_variant(name: str) -> str | None:
    """Return the variant by guessing from the name, or give up and return None."""
    parts = name.split("_")
    if len(parts) < 3:
        return None
    project_prefix, *variant_parts = parts
    comparison_string = "_".join(variant_parts)

    for variant_string, variant in {
        "STK_NEED": "StakeholderNeed",
        "STK_REQ": "StakeholderRequirement",
        "SYS_REQ": "SystemRequirement",
        "SYS_ELEMENT": "SystemElement",
        "SW_REQ": "SoftwareRequirement",
        "SW_ARCH": "SoftwareArchitecture",
        "SW_COMP": "SoftwareComponent",
        "SW_UNIT": "SoftwareUnit",
        "SW_UNIT_TEST": "SoftwareUnitTest",
        "SW_INT_TEST": "SoftwareIntegrationTest",
        "SW_QUAL_TEST": "SoftwareQualificationTest",
        "SYS_INT_TEST": "SystemIntegrationTest",
        "SYS_QUAL_TEST": "SystemQualificationTest",
        }.items():
        if comparison_string.startswith(variant_string):
            return variant
    return None


@lru_cache
def _get_section_mapping() -> dict[str, str]:
    mapping = {
        "Safety related": "qualification_related",
        "Qualification related": "qualification_related",
        "TQP related": "qualification_related",
        "TCL related": "qualification_related",
        "Derived from": "derived_from",
        "Fulfils": "fulfils",
        "Fulfilled by": "fulfilled_by",
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
