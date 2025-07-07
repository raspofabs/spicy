# Stakeholder needs

This is an extremely simple spec that fulfils all requirements.
POS is the Simple positive test data

## BDLNK_STK_NEED_have_a_stakeholder_need

The **STAKEHOLDER** needs **POS** to have a spec.

Elicitation date: March 2020

Qualification relevant: no

## BDLNK_STK_NEED_have_a_safety_need

The **STAKEHOLDER** needs **POS** to have safety as a concern.

Elicitation date: April 2020

Qualification relevant: yes

## BDLNK_STK_REQ_have_a_stakeholder_requirement

**POS** must have stakeholder needs refined into stakeholder requirements.

Implements:

- BDLNK_STK_NEED_have_a_stakeholder_need

Qualification relevant: no

## BDLNK_STK_REQ_safe_stakeholder_requirement

**POS** must be safe.

Implements:

- [BDLNK_STK_NEED_have_a_safety_need](bad_link.md#weird-fragment)

Qualification relevant: yes

# System level requirements

## BDLNK_SYS_REQ_have_a_sys_req

**POS** must support system requirements.

Verification criteria:

- This document should exist.

Derived from:

- [BDLNK_STK_REQ_have_a_stakeholder_requirement](complete_spec.md#bdlnk_stk_req_have_a_stakeholder_requirement)
- [BDLNK_STK_REQ_safe_stakeholder_requirement](complete_spec.md#bdlnk_stk_req_safe_stakeholder_requirement)

### Specification

- **Requirement type:** Qualification.
- **Interaction:** No interactions.
- **Constraints:** None
- **Operational and environmental limits and capabilities:** None.
- **Documentation:** Just this document.
- **Qualification relevant:** Yes.
- **Auditable:** No.

## BDLNK_SYS_ELEMENT_the_spec

This document is the realisation of this spec.

Software element: no

Implements:

- [BDLNK_SYS_REQ_have_a_sys_req](complete_spec.md#bdlnk_sys_req_have_a_sys_req)

## BDLNK_SYS_ELEMENT_the_software

There is no real software.

Software element: yes

Implements:

- [BDLNK_SYS_REQ_have_a_sys_req](complete_spec.md#bdlnk_sys_req_have_a_sys_req)

## BDLNK_SYS_INT_integrate_to_a_complete_spec

It's very easy to integrate a two element system.

Integrates:

- [BDLNK_SYS_ELEMENT_the_spec](complete_spec.md#bdlnk_sys_element_the_spec)
- [BDLNK_SYS_ELEMENT_the_software](complete_spec.md#bdlnk_sys_element_the_software)

Cases:

- BDLNK_SYS_INT_TEST_check_the_document_connectivity

Results:

- BDLNK_SYS_INT_TEST_check_the_document_connectivity: PASS

## BDLNK_SYS_QUAL_has_a_qualification_test

Test that this spec exists.

Qualification relevant: yes

Tests:

- [BDLNK_SYS_REQ_have_a_sys_req](complete_spec.md#bdlnk_sys_req_have_a_sys_req)

Cases:

- BDLNK_SYS_TEST_read_this_document

Results:

- BDLNK_SYS_TEST_read_this_document: PASS

# Validation - new to ASPICE 4.0

## BDLNK_VAL_document_is_provided

This test verifies the document is provisioned with the spicy toolkit.

Tests:

- [BDLNK_STK_REQ_have_a_stakeholder_requirement](complete_spec.md#bdlnk_stk_req_have_a_stakeholder_requirement)
- [BDLNK_STK_REQ_safe_stakeholder_requirement](complete_spec.md#bdlnk_stk_req_safe_stakeholder_requirement)

Cases:

- BDLNK_VAL_TEST_document_in_test_data
    1. Check that this document is provided in the spicy repo under the test data directory.

Results:

- BDLNK_VAL_TEST_document_in_test_data: PASS

# Software section

## BDLNK_SW_REQ_have_some_software

The **POS** has a software element

Decomposes:

- [BDLNK_SYS_ELEMENT_the_software](complete_spec.md#bdlnk_sys_element_the_software)

Realises:

- [BDLNK_SYS_REQ_have_a_sys_req](complete_spec.md#bdlnk_sys_req_have_a_sys_req)

## BDLNK_SW_ARCH_use_two_components

The **POS** uses two software components to realise the spec so it can have a
component integration spec.

Fulfils:

- [BDLNK_SW_REQ_have_some_software](complete_spec.md#bdlnk_sw_req_have_some_software)

## BDLNK_SW_COMP_primary_component

Implements:

- [BDLNK_SW_ARCH_use_two_components](complete_spec.md#bdlnk_sw_arch_use_two_components)

Fulfils:

- [BDLNK_SW_REQ_have_some_software](complete_spec.md#bdlnk_sw_req_have_some_software)

## BDLNK_SW_COMP_secondary_component

Implements:

- [BDLNK_SW_ARCH_use_two_components](complete_spec.md#bdlnk_sw_arch_use_two_components)

Fulfils:

- [BDLNK_SW_REQ_have_some_software](complete_spec.md#bdlnk_sw_req_have_some_software)

## BDLNK_SW_UNIT_primary_interface

Implements:

- [BDLNK_SW_COMP_primary_component](complete_spec.md#bdlnk_sw_comp_primary_component)

## BDLNK_SW_UNIT_primary_logic

Implements:

- [BDLNK_SW_COMP_primary_component](complete_spec.md#bdlnk_sw_comp_primary_component)

## BDLNK_SW_UNIT_secondary_interface

Implements:

- [BDLNK_SW_COMP_secondary_component](complete_spec.md#bdlnk_sw_comp_secondary_component)

## BDLNK_SW_UNIT_secondary_logic

Implements:

- [BDLNK_SW_COMP_secondary_component](complete_spec.md#bdlnk_sw_comp_secondary_component)

## Unit tests

### BDLNK_SW_UNIT_TEST_primary_interface

Tests:

- [BDLNK_SW_UNIT_primary_interface](complete_spec.md#bdlnk_sw_unit_primary_interface)

Cases:

- BDLNK_UNIT_TEST_a_test

Reults:

- BDLNK_UNIT_TEST_a_test: PASS

### BDLNK_SW_UNIT_TEST_primary_logic

Tests:

- [BDLNK_SW_UNIT_primary_logic](complete_spec.md#bdlnk_sw_unit_primary_logic)

Cases:

- BDLNK_UNIT_TEST_a_test

Reults:

- BDLNK_UNIT_TEST_a_test: PASS

### BDLNK_SW_UNIT_TEST_secondary_interface

Tests:

- [BDLNK_SW_UNIT_secondary_interface](complete_spec.md#bdlnk_sw_unit_secondary_interface)

Cases:

- BDLNK_UNIT_TEST_a_test

Reults:

- BDLNK_UNIT_TEST_a_test: PASS

### BDLNK_SW_UNIT_TEST_secondary_logic

Tests:

- [BDLNK_SW_UNIT_secondary_logic](complete_spec.md#bdlnk_sw_unit_secondary_logic)

Cases:

- BDLNK_UNIT_TEST_a_test

Reults:

- BDLNK_UNIT_TEST_a_test: PASS

## Unit integration

### BDLNK_SW_UNIT_INT_integrate_primary

Integrates:

- [BDLNK_SW_UNIT_primary_interface](complete_spec.md#bdlnk_sw_unit_primary_interface)
- [BDLNK_SW_UNIT_primary_logic](complete_spec.md#bdlnk_sw_unit_primary_logic)

### BDLNK_SW_UNIT_INT_integrate_secondary

Integrates:

- [BDLNK_SW_UNIT_secondary_interface](complete_spec.md#bdlnk_sw_unit_secondary_interface)
- [BDLNK_SW_UNIT_secondary_logic](complete_spec.md#bdlnk_sw_unit_secondary_logic)

## Component tests

### BDLNK_SW_COMP_TEST_primary_test

Tests:

- [BDLNK_SW_COMP_primary_component](complete_spec.md#bdlnk_sw_comp_primary_component)

Cases:

- BDLNK_TEST_primary_function

Results:

- BDLNK_TEST_primary_function: PASS

### BDLNK_SW_COMP_TEST_secondary_test

Tests:

- [BDLNK_SW_COMP_secondary_component](complete_spec.md#bdlnk_sw_comp_secondary_component)

Cases:

- BDLNK_TEST_secondary_function

Results:

- BDLNK_TEST_secondary_function: PASS

## BDLNK_SW_INT_integrate_everything

Integrates:

- [BDLNK_SW_COMP_primary_component](complete_spec.md#bdlnk_sw_comp_primary_component)
- [BDLNK_SW_COMP_secondary_component](complete_spec.md#bdlnk_sw_comp_secondary_component)


## BDLNK_SW_QUAL_test_the_software

Tests:

- [BDLNK_SW_REQ_have_some_software](complete_spec.md#bdlnk_sw_req_have_some_software)

Cases:

- BDLNK_TEST_check_software_is_present

Results:

- BDLNK_TEST_check_software_is_present: PASS

# Use case section

## Need to show how spicy works

    ID: FEAT_PRESENT_A_SPEC

A developer wants to see a complete positive example.

Fulfils:

- [BDLNK_STK_NEED_have_a_stakeholder_need](complete_spec.md#bdlnk_stk_need_have_a_stakeholder_need)

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

    BDLNK_STK_NEED_have_a_safety_need

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
