# Stakeholder requirements

## SPICY_STK_REQ_spec_traceability

The **SPICY** tool must be able to identify missing or inconsistent links in the
documentation between elements requiring bi-directional traceability.

The inverse is also required. **SPICY** must not enforce any missing but
implied spec elements that are not required.

Examples would include the detailed design of any referenced software unit or
the system requirement from which a software requirement was derived.

Qualification relevant: yes

Implements:

- [SPICY_STK_NEED_verify_traceability](/spicy_spec/stakeholder_needs.md#spicy_stk_need_verify_traceability)
- [SPICY_STK_NEED_verify_completeness](/spicy_spec/stakeholder_needs.md#spicy_stk_need_verify_completeness)

## SPICY_STK_REQ_verify_correctness

The **SPICY** to identify elements with incorrect structure,
omitting important details, or duplicating data.

Qualification relevant: yes

Implements:

- [SPICY_STK_NEED_verify_correctness](/spicy_spec/stakeholder_needs.md#spicy_stk_need_verify_correctness)

## SPICY_STK_REQ_aspice_compatibility

The **SPICY** tool must verify against
the Spec Elements and Links suggested by ASPICE 4.0.

Qualification relevant: yes

Implements:

- [SPICY_STK_NEED_aspice_compatibility](/spicy_spec/stakeholder_needs.md#spicy_stk_need_aspice_compatibility)

## SPICY_STK_REQ_ISO_26262_tool_qualification

The **SPICY** tool must be able to connect
the ASPICE elements and links with
an ISO26262 style Use-case spec
to support a _use-case_ based approach to tool qualification.

Qualification relevant: yes

Implements:

- [SPICY_STK_NEED_ISO_26262_tool_qualification](/spicy_spec/stakeholder_needs.md#spicy_stk_need_iso_26262_tool_qualification)

## SPICY_STK_REQ_document_rendering_support

The **SPICY** tool should verify and fix any broken links in the rendering
of the document to help make moving between elements easier.

Qualification relevant: no

Implements:

- [SPICY_STK_NEED_document_rendering_support](/spicy_spec/stakeholder_needs.md#spicy_stk_need_document_rendering_support)

## SPICY_STK_REQ_architectural_decision_records

The **SPICY** tool should enforce architectural decisions are made and recorded.

Qualification relevant: no

Implements:

- [SPICY_STK_NEED_architectural_decision_records](/spicy_spec/stakeholder_needs.md#spicy_stk_need_architectural_decision_records)
