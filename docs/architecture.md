# Spicy architecture

The general approach is to read all the md files you can find, assuming that
the specs are not located in specific files.
This means an ASPICE V structured document set can be parsed, but so can a
stakeholder need to validation per document.

# Recognising specs

A spec is recognised by pattern matching with a simple formula:

`<PROJECT_PREFIX>_<SPEC_PREFIX>_the_rest_of_the_spec`

Requiring the project prefix helps disambiguate when there might be more than
one project concurrent in the documentation. This can happen for various
reasons, including the possibility of needs tracing from another project or
using another project to satisfy requirements in the one under inspection.

Specs are expected to not overlap, so some assumptions have been made regarding
the document structure. These assumptions might cause the errors presented to
look wrong if the structure is not observed, but this is much like parenthesis
syntax errors, and probably not solvable.


1. Whenever a heading matches a spec pattern,
    - a spec is opened and the parsing class is detected from the spec pattern.
    - the _heading level_ is stored to determine later actions. 
2. (redundant rule for clarification) If a new heading at the same or lower
   level matches a spec pattern, it is assumed that the current spec has ended.
   For example, if the current spec was originally seen at H2,
   and if a new spec is seen at H2 or H3,
   then the current spec shall be closed and a new spec shall be opened with
   the new _heading level_.
3. When the parser sees a new heading at the same level or higher, regardless
   of whether it matches the spec pattern or not, the spec is closed.
   This allows for mid-document note sections to use a higher level heading and
   not accidentally contribute to the previous spec.
