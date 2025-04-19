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

- POS_STK_NEED_have_a_stakeholder_need

Qualification relevant: no

## POS_STK_REQ_safe_stakeholder_requirement

**POS** must be safe.

Implements:

- POS_STK_NEED_have_a_safety_need

Qualification relevant: yes

# System level requirements

## POS_SYS_REQ_have_a_sys_req

**POS** must support system requirements.

Verification criteria:

- This document should exist.

Derived from:

- POS_STK_REQ_have_a_stakeholder_requirement
- POS_STK_REQ_safe_stakeholder_requirement

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

- POS_SYS_REQ_have_a_sys_req

## POS_SYS_ELEMENT_the_software

There is no real software.

Software element: yes

Implements:

- POS_SYS_REQ_have_a_sys_req

## POS_SYS_INT_integrate_to_a_complete_spec

It's very easy to integrate a two element system.

Integrates:

- POS_SYS_ELEMENT_the_spec
- POS_SYS_ELEMENT_the_software

Cases:

- POS_SYS_INT_TEST_check_the_document_connectivity

Results:

- POS_SYS_INT_TEST_check_the_document_connectivity: PASS

## POS_SYS_QUAL_has_a_qualification_test

Test that this spec exists.

Qualification relevant: yes

Tests:

- POS_SYS_REQ_have_a_sys_req

Cases:

- POS_SYS_TEST_read_this_document

Results:

- POS_SYS_TEST_read_this_document: PASS

# Validation - new to ASPICE 4.0

## POS_VAL_document_is_provided

This test verifies the document is provisioned with the spicy toolkit.

Tests:

- POS_STK_REQ_have_a_stakeholder_requirement

Cases:

- POS_VAL_TEST_document_in_test_data
    1. Check that this document is provided in the spicy repo under the test data directory.

Results:

- POS_VAL_TEST_document_in_test_data: PASS

# Software section

## POS_SW_REQ_have_some_software

The **POS** has a software element

Decomposes:

- [POS_SYS_ELEMENT_the_software](#pos_sys_element_the_software)

Realises:

- [POS_SYS_REQ_have_a_sys_req](#pos_sys_req_have_a_sys_req)

# Use case section

## Need to show how spicy works

    ID: FEAT_PRESENT_A_SPEC

A developer wants to see a complete positive example.

Fulfils:

    POS_STK_NEED_have_a_stakeholder_need

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

    POS_STK_NEED_have_a_stakeholder_need
    POS_STK_NEED_have_a_safety_need

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
