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
