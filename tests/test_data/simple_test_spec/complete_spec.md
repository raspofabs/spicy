# Stakeholder needs

This is an extremely simple spec that fulfils all requirements.
POS is the Simple positive test data

## POS_STK_NEED_have_a_stakeholder_need

The **STAKEHOLDER** needs **POS** to have a spec.

Elicitation date: March 2020

Qualification relevant: no

## POS_STK_NEED_have_a_safety_need

The **STAKEHOLDER** needs **POS** to have safety as a concern.

Elicitation date: April 2020

Qualification relevant: yes

## POS_STK_REQ_have_a_stakeholder_requirement

**POS** must have stakeholder needs refined into stakeholder requirements.

Implements:

- [POS_STK_NEED_have_a_stakeholder_need](complete_spec.md#pos_stk_need_have_a_stakeholder_need)

Qualification relevant: no

## POS_STK_REQ_safe_stakeholder_requirement

**POS** must be safe.

Implements:

- [POS_STK_NEED_have_a_safety_need](complete_spec.md#pos_stk_need_have_a_safety_need)

Qualification relevant: yes

# System level requirements

## POS_SYS_REQ_have_a_sys_req

**POS** must support system requirements.

Verification criteria:

- This document should exist.

Derived from:

- [POS_STK_REQ_have_a_stakeholder_requirement](complete_spec.md#pos_stk_req_have_a_stakeholder_requirement)
- [POS_STK_REQ_safe_stakeholder_requirement](complete_spec.md#pos_stk_req_safe_stakeholder_requirement)

### Specification

- **Requirement type:** Qualification.
- **Interaction:** No interactions.
- **Constraints:** None
- **Operational and environmental limits and capabilities:** None.
- **Documentation:** Just this document.
- **Qualification relevant:** Yes.
- **Auditable:** No.

## POS_SYS_ELEMENT_the_spec

This document is the realisation of this spec.

Software element: no

Implements:

- [POS_SYS_REQ_have_a_sys_req](complete_spec.md#pos_sys_req_have_a_sys_req)

## POS_SYS_ELEMENT_the_software

There is no real software.

Software element: yes

Implements:

- [POS_SYS_REQ_have_a_sys_req](complete_spec.md#pos_sys_req_have_a_sys_req)

## POS_SYS_INT_integrate_to_a_complete_spec

It's very easy to integrate a two element system.

Integrates:

- [POS_SYS_ELEMENT_the_spec](complete_spec.md#pos_sys_element_the_spec)
- [POS_SYS_ELEMENT_the_software](complete_spec.md#pos_sys_element_the_software)

Cases:

- POS_SYS_INT_TEST_check_the_document_connectivity

Results:

- POS_SYS_INT_TEST_check_the_document_connectivity: PASS

## POS_SYS_QUAL_has_a_qualification_test

Test that this spec exists.

Qualification relevant: yes

Tests:

- [POS_SYS_REQ_have_a_sys_req](complete_spec.md#pos_sys_req_have_a_sys_req)

Cases:

- POS_SYS_TEST_read_this_document

Results:

- POS_SYS_TEST_read_this_document: PASS

# Validation - new to ASPICE 4.0

## POS_VAL_document_is_provided

This test verifies the document is provisioned with the spicy toolkit.

Tests:

- [POS_STK_REQ_have_a_stakeholder_requirement](complete_spec.md#pos_stk_req_have_a_stakeholder_requirement)
- [POS_STK_REQ_safe_stakeholder_requirement](complete_spec.md#pos_stk_req_safe_stakeholder_requirement)

Cases:

- POS_VAL_TEST_document_in_test_data
    1. Check that this document is provided in the spicy repo under the test data directory.

Results:

- POS_VAL_TEST_document_in_test_data: PASS

# Software section

## POS_SW_REQ_have_some_software

The **POS** has a software element

Decomposes:

- [POS_SYS_ELEMENT_the_software](complete_spec.md#pos_sys_element_the_software)

Realises:

- [POS_SYS_REQ_have_a_sys_req](complete_spec.md#pos_sys_req_have_a_sys_req)

## POS_SW_ARCH_use_two_components

The **POS** uses two software components to realise the spec so it can have a
component integration spec.

Fulfils:

- [POS_SW_REQ_have_some_software](complete_spec.md#pos_sw_req_have_some_software)

## POS_SW_COMP_primary_component

Implements:

- [POS_SW_ARCH_use_two_components](complete_spec.md#pos_sw_arch_use_two_components)

Fulfils:

- [POS_SW_REQ_have_some_software](complete_spec.md#pos_sw_req_have_some_software)

## POS_SW_COMP_secondary_component

Implements:

- [POS_SW_ARCH_use_two_components](complete_spec.md#pos_sw_arch_use_two_components)

Fulfils:

- [POS_SW_REQ_have_some_software](complete_spec.md#pos_sw_req_have_some_software)

## POS_SW_UNIT_primary_interface

Implements:

- [POS_SW_COMP_primary_component](complete_spec.md#pos_sw_comp_primary_component)

## POS_SW_UNIT_primary_logic

Implements:

- [POS_SW_COMP_primary_component](complete_spec.md#pos_sw_comp_primary_component)

## POS_SW_UNIT_secondary_interface

Implements:

- [POS_SW_COMP_secondary_component](complete_spec.md#pos_sw_comp_secondary_component)

## POS_SW_UNIT_secondary_logic

Implements:

- [POS_SW_COMP_secondary_component](complete_spec.md#pos_sw_comp_secondary_component)

## Unit tests

### POS_SW_UNIT_TEST_primary_interface

Tests:

- [POS_SW_UNIT_primary_interface](complete_spec.md#pos_sw_unit_primary_interface)

Cases:

- POS_UNIT_TEST_a_test

Reults:

- POS_UNIT_TEST_a_test: PASS

### POS_SW_UNIT_TEST_primary_logic

Tests:

- [POS_SW_UNIT_primary_logic](complete_spec.md#pos_sw_unit_primary_logic)

Cases:

- POS_UNIT_TEST_a_test

Reults:

- POS_UNIT_TEST_a_test: PASS

### POS_SW_UNIT_TEST_secondary_interface

Tests:

- [POS_SW_UNIT_secondary_interface](complete_spec.md#pos_sw_unit_secondary_interface)

Cases:

- POS_UNIT_TEST_a_test

Reults:

- POS_UNIT_TEST_a_test: PASS

### POS_SW_UNIT_TEST_secondary_logic

Tests:

- [POS_SW_UNIT_secondary_logic](complete_spec.md#pos_sw_unit_secondary_logic)

Cases:

- POS_UNIT_TEST_a_test

Reults:

- POS_UNIT_TEST_a_test: PASS

## Unit integration

### POS_SW_UNIT_INT_integrate_primary

Integrates:

- [POS_SW_UNIT_primary_interface](complete_spec.md#pos_sw_unit_primary_interface)
- [POS_SW_UNIT_primary_logic](complete_spec.md#pos_sw_unit_primary_logic)

### POS_SW_UNIT_INT_integrate_secondary

Integrates:

- [POS_SW_UNIT_secondary_interface](complete_spec.md#pos_sw_unit_secondary_interface)
- [POS_SW_UNIT_secondary_logic](complete_spec.md#pos_sw_unit_secondary_logic)

## Component tests

### POS_SW_COMP_TEST_primary_test

Tests:

- [POS_SW_COMP_primary_component](complete_spec.md#pos_sw_comp_primary_component)

Cases:

- POS_TEST_primary_function

Results:

- POS_TEST_primary_function: PASS

### POS_SW_COMP_TEST_secondary_test

Tests:

- [POS_SW_COMP_secondary_component](complete_spec.md#pos_sw_comp_secondary_component)

Cases:

- POS_TEST_secondary_function

Results:

- POS_TEST_secondary_function: PASS

## POS_SW_INT_integrate_everything

Integrates:

- [POS_SW_COMP_primary_component](complete_spec.md#pos_sw_comp_primary_component)
- [POS_SW_COMP_secondary_component](complete_spec.md#pos_sw_comp_secondary_component)


## POS_SW_QUAL_test_the_software

Tests:

- [POS_SW_REQ_have_some_software](complete_spec.md#pos_sw_req_have_some_software)

Cases:

- POS_TEST_check_software_is_present

Results:

- POS_TEST_check_software_is_present: PASS

# Use case section

## Need to show how spicy works

    ID: FEAT_PRESENT_A_SPEC

A developer wants to see a complete positive example.

Fulfils:

- [POS_STK_NEED_have_a_stakeholder_need](complete_spec.md#pos_stk_need_have_a_stakeholder_need)

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

- [POS_STK_NEED_have_a_safety_need](complete_spec.md#pos_stk_need_have_a_safety_need)

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
