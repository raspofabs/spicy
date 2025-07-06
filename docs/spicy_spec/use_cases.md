# Qualifying a tool

<!-- toc -->

The **TQM** needs to be able to verify the documentation is ASPICE and ISO26262 compliant.
The **TWs** need support in writing the necessary documentation.

# Verification of documentation for tool qualification

    ID: FEAT_DOCUMENTATION_CHECK

A **TQM** will use the spicy tool to produce a compliance check result.

Fulfils:

    SPICY_STK_NEED_verify_traceability
    SPICY_STK_NEED_verify_correctness
    SPICY_STK_NEED_verify_completeness
    SPICY_STK_NEED_ISO_26262_tool_qualification
    SPICY_STK_NEED_aspice_compatibility

## Features, functions, and technical properties

**Spicy** must produce a convincing report, detailing the findings from the
check, listing what was found, how many of each type and the current status of
the tool (PASS/FAIL)

## Description of usage

- **Purpose:** To guide the technical writers in finding gaps in the documentation or incorrectly formatted elements.
- **Inputs:** The project configuration parameters and the documentation files.
- **Outputs:** A report indicating any missing or misconfigured items.
- **Usage procedure:** Run the spicy tool, providing the configuration parameters and path to the documentation files.
- **Environmental constraints:**
  The tool must run standalone and not need the documentation to be pre-parsed into a different format.
  The tool should work as a headless command line tool so it can run in CI.
  The tool should run on Linux (Ubuntu will be a validated test environment)

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


# Reviewing documentation for the tool

    ID: FEAT_DOCUMENTATION_REVIEW

A **TQM** will use a tool to render a live version of the system and software
spec and the qualification plan documents to help argue the ASPICE compliance
against an ASPICE assessor.

Fulfils:

    SPICY_STK_NEED_document_rendering_support

## Features, functions, and technical properties

**Spicy** docs must be supported such that the rendered document's links are
easy to traverse and can quickly answer any questions put forth by an ASPICE
assessor.

## Description of usage

- **Purpose:** To support developers defending an ASPICE audit.
- **Inputs:** The project configuration parameters and the documentation files.
- **Outputs:** Runtime errors and an interactive document realised through direct GUI or restful web-page server.
- **Usage procedure:** Run the spicy audit tool, providing the configuration parameters and path to the documentation files.
- **Environmental constraints:**
  The tool must run standalone and not need the documentation to be pre-parsed into a different format.
  The tool should work either as a GUI application, or as a headless server so a developer can browse from another machine.
  The tool should run on Linux (Ubuntu will be a validated test environment)

## Impact analysis of feature

    TI class: TI2

If there were errors in the linkage in the rendered document, then they would
not help defend the case for ASPICE compliance.
Being able to track back and forth between requirements and implementations and
tests is important to argue that we know that all our requirements are fully
linked.

## Detectability analysis of feature

    TD class: TD1

Bad links in general are easy to spot, but the occasional error is unlikely, so
the chance that an error in a particular type of spec only is not detected is low.
