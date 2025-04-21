# Stakeholder needs

SPICY is the system for checking whether you have a complete set of consistent
documents sufficient for your software tool.
The sufficiency requirements are adapted from ASPICE 4.0.

Stakeholders include:

- **Technical writers (TW):** They develop the documents required for the
  tools. This role can be assigned to a developer of the tool.
- **Tool Qualification Manager (TQM):** They verify all software tools used in
  a software development project meet the agreed qualification criteria.
  They review the qualification plan for consistency.
  They review the results of the application of the qualification methods for
  whether the tool currently qualifies for use in the project.

Concepts:

- Spec Element (or simply Element): a need, requirement, design or other
  linkable node in the documentation. These would normally be numbered in most
  documentation systems, but it's the (strong) opinion of this author that
  numbers are a bit annoying and offer no real benefit.
  I gained this opinion through years of game development where "level 3" was
  only really level 3 for a few iterations. At the end of any project of
  sufficient duration, you either renumber the levels multiple times, or you
  stop caring and end up with level numbers  like "level 2, level 3, level 1,
  level 3b, level 5, level 8, level last, level 7."
- Link: a link is a reference to another Spec Element for some purpose.
  Stakeholder Needs must be broken down or refined into Stakeholder Requirements.
  For consistency, there must be links pointing from Stakeholder Needs to Stakeholder requirements.
  Links have consistency requirements too.
  Each Stakeholder Need must link to at least one Stakeholder Requirement as implemented by, and
  each Stakeholder Requirement must link to at least one Stakeholder Need as implements.
- Cases: in test specs, there are test cases.
  These are the ways to verify the requirement is fulfilled.
- Results: in test specs, each test case needs the test results.
  These are used to validate the implementation.

## SPICY_STK_NEED_verify_traceability

The **TWs** need **SPICY** to identify missing or inconsistent links in the
documentation between elements requiring bi-directional traceability.

Elicitation date: 2025-04-05

Qualification relevant: yes

## SPICY_STK_NEED_verify_correctness

The **TWs** need **SPICY** to identify elements with incorrect structure,
omitting important details, or duplicating data.

Elicitation date: 2025-04-05

Qualification relevant: yes

## SPICY_STK_NEED_verify_completeness

The **TWs** need **SPICY** to identify elements lacking the necessary linkage
to other spec elements needed to fulfil their specification.

Elicitation date: 2025-04-05

Qualification relevant: yes

## SPICY_STK_NEED_aspice_compatibility

The **TQM** needs **SPICY** to verify the Spec Elements and Links suggested by
ASPICE are found in the documentation under inspection.

Note: The version of ASPICE referenced should be at least ASPICE 4.0.

Elicitation date: 2025-04-05

Qualification relevant: yes

## SPICY_STK_NEED_ISO_26262_tool_qualification

The **TQM** needs **SPICY** to incorporate the necessary specs to support a
_use-case_ based approach to tool qualification.

ISO-26262 suggests listing use cases based on a user manual, software spec, and
interviews with the tool stakeholders.
The outcome of this process is a list of use-cases.
The **TWs** must document the details,
classify the Tool's Impact (TI),
classify the Tool's error Detectability (TD),
and then calculate the Tool Confidence Level (TCL).
This level is counterintuitively inverted with TCL1 being a low TCL, but that
means you only need low confidence. TCL3 means you need high confidence.

Any tool with a medium (TCL2) or high (TCL3) needs some way to gain that
required level of confidence.
Methods to achieve that level include "confidence
from use" which means that it's been used by so many for so long that the
likelihood of unknown bugs or limitations is low enough you use the tool with
high confidence or can plan around the known issues.
Examples of this can be using an old well-used tool like gcov, gtest, sed, awk,
or grep, where the total number of hours of use by the tool is in the millions
of hours across many architectures and use case patterns.
Other ways to gain confidence include having a well defined and documented development process, and follow it.
In this system, we follow a variant of ASPICE to provide a framework for structuring the work to be completed.
Another way to gain confidence is through software inspection. This can include
tests, static analysis, review, linters, or any other software quality tools.
For this project, the latter two are used because they provide a way to
bootstrap the purpose of the tool.

Elicitation date: 2025-04-05

Qualification relevant: yes

## SPICY_STK_NEED_document_rendering_support

The **TWs** need **SPICY** to verify and fix any broken links in the rendering
of the document to help make moving between elements easier.

The documents must be cross-linked between elements for bi-directional
traceability, but having the links be hyperlinks you can click to take you to
the other elements will help simplify the job of reviewing items and argue the
case for ASPICE compliance against an ASPICE assessor.

Elicitation date: 2025-04-05

Qualification relevant: no

## SPICY_STK_NEED_architectural_decision_records

The **TWs** need **SPICY** to enforce architectural decisions are made and recorded.

Architectural decisions are those which affect the selection process for
solutions lower down in the process.
For example, with **SPICY**, there was an architectural decision to develop a
solution which takes markdown files as input.
The markdown would be parsed and generates a model from that textual content.
Only when the model was created would the issues be rendered.

This decision was taken for reasons, but those reasons were not written down at the time.

This need explicitly requires that any architectural decisions are recorded.
Alternatives must be considered.
Any costs associated with the decision and the payoff are documented.

Architectural decisions without a downside or payoff are unlikely to be
architectural decisions, so this need relates to completeness in the negative.
It helps identify overspecification.

Elicitation date: 2025-04-13

Qualification relevant: no
