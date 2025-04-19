# Stakeholder needs

ASPICE calls them _requests_, but they could also be referred to as INCOSE
_needs_ statements* .
The needs are distilled from the expectations and requests in the surveys, and
from the experience of the system architect.

Each stakeholder need and requirement includes an ID and a statement.

The ID is in the form `TLA_STK_NEED_<Unique Name>`
or `TLA_STK_REQ_<Unique Name>`
The lack of IDs allows for a natural ordering and inserting new requirements
without fussing with numbers or dislocation as they are revealed during
customer feedback in the course of agile development.

The needs statement is formatted, "The <stakeholder(s)> needs the <entity> to ..."
e.g. "The _Captain_ needs the _ship_ to reach at least 30 knots when on calm seas."
These can be transformed into requirements statements, "The <entity> shall ..."
e.g. "The _ship_ shall attain a nautical speed of at least 30 knots when operated at full power for one minute from a standstill in calm seas conditions."

\* Definition of INCOSE needs: [chapter 1.6.3](https://www.incose.org/docs/default-source/working-groups/requirements-wg/gtwr/incose_rwg_gtwr_v4_040423_final_drafts.pdf?sfvrsn=5c877fc7_2).

## Basic needs

### TLA_STK_NEED_a_stakeholder_need

The **USER** needs the **TLA** to do a thing.

Elicitation date: January 1970

Qualification relevant: yes

Interpreted by:

- TLA_STK_REQ_1_numbered_requirements
