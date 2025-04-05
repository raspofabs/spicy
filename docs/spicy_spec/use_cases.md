# Qualifying a tool

<!-- toc -->

The **TQM** needs to be able to verify the documentation is ASPICE and ISO26262 compliant.
The **TWs** need support in writing the necessary documentation.

# Order a cookie for delivery on the web-page

    ID: FEAT_DOCUMENTATION_CHECK

A **TQM** will use the spicy tool to produce a compliance check result.

Fulfils:

    SPICY_STK_NEED_verify_traceability
    SPICY_STK_NEED_verify_correctness
    SPICY_STK_NEED_verify_completeness

## Features, functions, and technical properties

**Spicy** must produce a convincing report, detailing the findings from the
check, listing what was found, how many of each type and the current status of
the tool (PASS/FAIL)

## Description of usage

- **Purpose:**
- **Inputs:**
- **Outputs:**
- **Usage procedure:**
- **Environmental constraints:**

## Impact analysis of feature

    TI class: TI2

If there were errors in the tool, then an incorrectly documented, poorly tested
tool would appear to be valid, allowing the tool to be used when it should not.

## Detectability analysis of feature

    TD class: TD3

Analysis tools are prone to a general problem of difficulty in detecting errors
of omission, so errors stating that things are wrong would be easily detected,
but errors saying "nothing is wrong" when there were problems, those could
easily be missed.
