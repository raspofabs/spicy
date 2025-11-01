# Stakeholder needs

This is an extremely simple spec that fulfils all requirements.
POS is the Simple positive test data

## FIXME_STK_NEED_have_a_stakeholder_need

The **STAKEHOLDER** needs **POS** to have a spec.

Elicitation date: March 2020

Qualification relevant: no

## FIXME_STK_NEED_have_a_safety_need

The **STAKEHOLDER** needs **POS** to have safety as a concern.

Elicitation date: April 2020

Qualification relevant: yes

## FIXME_STK_REQ_have_a_stakeholder_requirement

**POS** must have stakeholder needs refined into stakeholder requirements.

Implements:

- FIXME_STK_NEED_have_a_stakeholder_need

Qualification relevant: no

## FIXME_STK_REQ_safe_stakeholder_requirement

**POS** must be safe.

Implements:

- [FIXME_STK_NEED_have_a_safety_need](bad_link.md#weird-fragment)

Qualification relevant: yes

# System level requirements

## FIXME_SYS_REQ_have_a_sys_req

**POS** must support system requirements.

Verification criteria:

- This document should exist.

Derived from:

- [FIXME_STK_REQ_have_a_stakeholder_requirement](complete_spec.md#fixme_stk_req_have_a_stakeholder_requirement)
- [FIXME_STK_REQ_safe_stakeholder_requirement](complete_spec.md#fixme_stk_req_safe_stakeholder_requirement)

### Specification

- **Requirement type:** Qualification.
- **Interaction:** No interactions.
- **Constraints:** None
- **Operational and environmental limits and capabilities:** None.
- **Documentation:** Just this document.
- **Qualification relevant:** Yes.
- **Auditable:** No.

## FIXME_SYS_ELEMENT_the_spec

This document is the realisation of this spec.

Software element: no

Implements:

- [FIXME_SYS_REQ_have_a_sys_req](complete_spec.md#fixme_sys_req_have_a_sys_req)

## FIXME_SYS_ELEMENT_the_software

There is no real software.

Software element: yes

Implements:

- [FIXME_SYS_REQ_have_a_sys_req](complete_spec.md#fixme_sys_req_have_a_sys_req)

## FIXME_SYS_INT_integrate_to_a_complete_spec

It's very easy to integrate a two element system.

Integrates:

- [FIXME_SYS_ELEMENT_the_spec](complete_spec.md#fixme_sys_element_the_spec)
- [FIXME_SYS_ELEMENT_the_software](complete_spec.md#fixme_sys_element_the_software)

## FIXME_SYS_QUAL_has_a_qualification_test

Test that this spec exists.

Qualification relevant: yes

Tests:

- [FIXME_SYS_REQ_have_a_sys_req](complete_spec.md#fixme_sys_req_have_a_sys_req)

# Validation - new to ASPICE 4.0

## FIXME_VAL_document_is_provided

This test verifies the document is provisioned with the spicy toolkit.

Tests:

- [FIXME_STK_REQ_have_a_stakeholder_requirement](complete_spec.md#fixme_stk_req_have_a_stakeholder_requirement)
- [FIXME_STK_REQ_safe_stakeholder_requirement](complete_spec.md#fixme_stk_req_safe_stakeholder_requirement)

# Software section

## FIXME_SW_REQ_have_some_software

The **POS** has a software element

Decomposes:

- [FIXME_SYS_ELEMENT_the_software](complete_spec.md#fixme_sys_element_the_software)

Realises:

- [FIXME_SYS_REQ_have_a_sys_req](complete_spec.md#fixme_sys_req_have_a_sys_req)

## FIXME_SW_ARCH_use_two_components

The **POS** uses two software components to realise the spec so it can have a
component integration spec.

Fulfils:

- [FIXME_SW_REQ_have_some_software](complete_spec.md#fixme_sw_req_have_some_software)

## FIXME_SW_COMP_primary_component

Implements:

- [FIXME_SW_ARCH_use_two_components](complete_spec.md#fixme_sw_arch_use_two_components)

Fulfils:

- [FIXME_SW_REQ_have_some_software](complete_spec.md#fixme_sw_req_have_some_software)

## FIXME_SW_COMP_secondary_component

Implements:

- [FIXME_SW_ARCH_use_two_components](complete_spec.md#fixme_sw_arch_use_two_components)

Fulfils:

- [FIXME_SW_REQ_have_some_software](complete_spec.md#fixme_sw_req_have_some_software)

## FIXME_SW_UNIT_primary_interface

Implements:

- [FIXME_SW_COMP_primary_component](complete_spec.md#fixme_sw_comp_primary_component)

## FIXME_SW_UNIT_primary_logic

Implements:

- [FIXME_SW_COMP_primary_component](complete_spec.md#fixme_sw_comp_primary_component)

## FIXME_SW_UNIT_secondary_interface

Implements:

- [FIXME_SW_COMP_secondary_component](complete_spec.md#fixme_sw_comp_secondary_component)

## FIXME_SW_UNIT_secondary_logic

Implements:

- [FIXME_SW_COMP_secondary_component](complete_spec.md#fixme_sw_comp_secondary_component)

## Unit tests

### FIXME_SW_UNIT_TEST_primary_interface

Tests:

- [FIXME_SW_UNIT_primary_interface](complete_spec.md#fixme_sw_unit_primary_interface)

### FIXME_SW_UNIT_TEST_primary_logic

Tests:

- [FIXME_SW_UNIT_primary_logic](complete_spec.md#fixme_sw_unit_primary_logic)

### FIXME_SW_UNIT_TEST_secondary_interface

Tests:

- [FIXME_SW_UNIT_secondary_interface](complete_spec.md#fixme_sw_unit_secondary_interface)

### FIXME_SW_UNIT_TEST_secondary_logic

Tests:

- [FIXME_SW_UNIT_secondary_logic](complete_spec.md#fixme_sw_unit_secondary_logic)

## Unit integration

### FIXME_SW_UNIT_INT_integrate_primary

Integrates:

- [FIXME_SW_UNIT_primary_interface](complete_spec.md#fixme_sw_unit_primary_interface)
- [FIXME_SW_UNIT_primary_logic](complete_spec.md#fixme_sw_unit_primary_logic)

### FIXME_SW_UNIT_INT_integrate_secondary

Integrates:

- [FIXME_SW_UNIT_secondary_interface](complete_spec.md#fixme_sw_unit_secondary_interface)
- [FIXME_SW_UNIT_secondary_logic](complete_spec.md#fixme_sw_unit_secondary_logic)

## Component tests

### FIXME_SW_COMP_TEST_primary_test

Tests:

- [FIXME_SW_COMP_primary_component](complete_spec.md#fixme_sw_comp_primary_component)

### FIXME_SW_COMP_TEST_secondary_test

Tests:

- [FIXME_SW_COMP_secondary_component](complete_spec.md#fixme_sw_comp_secondary_component)

## FIXME_SW_INT_integrate_everything

Integrates:

- [FIXME_SW_COMP_primary_component](complete_spec.md#fixme_sw_comp_primary_component)
- [FIXME_SW_COMP_secondary_component](complete_spec.md#fixme_sw_comp_secondary_component)


## FIXME_SW_QUAL_test_the_software

Tests:

- [FIXME_SW_REQ_have_some_software](complete_spec.md#fixme_sw_req_have_some_software)

# Use case section

## Need to show how spicy works

    ID: FEAT_PRESENT_A_SPEC

A developer wants to see a complete positive example.

Fulfils:

- [FIXME_STK_NEED_have_a_stakeholder_need](complete_spec.md#fixme_stk_need_have_a_stakeholder_need)

### Features, functions, and technical properties

The spec will be as simple as possible while remaining complete.

### Description of usage

- **Purpose:**
    To verify the positive case.
- **Inputs:**
    Just this spec file.
- **Outputs:**
    A happy output in spicy.
- **Usage procedure:**
    Run the tests.
- **Environmental constraints:**
    The spicy Python package.

### Impact analysis of feature

    TI class: TI2

If this spec is bad, then it won't test the positive path at all.

### Detectability analysis of feature

    TD class: TD1

But the point of tests is to test stuff.

## Must use spicy safely

    ID: FEAT_SAFE_SPEC

A developer wants to see how safety works.

Fulfils:

    FIXME_STK_NEED_have_a_safety_need

### Features, functions, and technical properties

The spec will be as simple as possible while remaining complete.

### Description of usage

- **Purpose:**
    To verify the positive case.
- **Inputs:**
    Just this spec file.
- **Outputs:**
    A happy output in spicy.
- **Usage procedure:**
    Run the tests.
- **Environmental constraints:**
    The spicy Python package.

### Impact analysis of feature

    TI class: TI2

If this spec is bad, then it won't test the positive path at all.

### Detectability analysis of feature

    TD class: TD2

Positive tests tend to be difficult to verify.
