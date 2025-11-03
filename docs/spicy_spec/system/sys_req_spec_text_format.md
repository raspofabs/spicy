# SPICY_SYS_REQ_spec_text_format

The textual form is based around headers and prefixes.
Some headers are explicit markdown headers, such as the `#` based headers.
Some headers are magic keyword based, such as the `Implements:` below.

```txt
## Basic requirements

### TLA_STK_REQ_1_numbered_requirements

**TLA** shall do a thing.

Qualification relevant: yes

Implements:

- [TLA_STK_NEED_get_a_cookie](#tla_stk_need_get_a_cookie)
```

This allows specs to nest and
be present in the same markdown file without interfering with each other.

Derived from:

- [SPICY_STK_REQ_spec_traceability](/spicy_spec/stakeholder_reqs.md#spicy_stk_req_spec_traceability)
- [SPICY_STK_REQ_aspice_compatibility](/spicy_spec/stakeholder_reqs.md#spicy_stk_req_aspice_compatibility)
