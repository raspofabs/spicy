# Attribute delegation

for every safety-related spec:
    they must be fulfilled by at least one safety-related spec.
for every security-related spec:
    they must be fulfilled by at least one security-related spec.

Any relevant spec can be tagged with safety-related or security related.
If it is, at least one fulfilment link must be tagged with the attribute.
A link tagged with the attribute will delegate the attribute to the fulfiller.

# Fulfilment

for every stakeholder_need:
    must be fulfilled by at least one stakeholder_requirement
for every stakeholder_requirement:
    must be fulfilled by at least one system_requirement
    every stakeholder_need it fulfils must exist

All links are bidirectional.
All links must lead from one spec item to another.
All linked spec items must exist.

# Some specs require certain other fields


Every stakeholder need should have an elicitation_date explaining when it was
first applied to the spec.

Every test requirement must have one or more specs that it tests.
Every test requirement must have one or more cases which test those specs.
Every test requirement must have a test result for each test case.

# Links mean something

Some links are connections:

A spec might implement, realize, resolve, fulfil, or deliver another spec.
A spec might refine or interpret another spec.
A spec might satisfy, another spec without explicitly attempting to resolve it.
A spec might break down or split into multiple specs for easier manipulation,
testing, or separation of concerns.
A spec might validate, verify, qualify, test, confirm, prove, demonstrate, assert or measure another spec.

A stakeholder need is refined into a stakeholder requirement.
This is a mandatory bidirectional link.

A use case fulfils a stakeholder need.
This is mandatory uni-directional link from the use-case.
Not all stakeholder needs require a tool qualification use-case.

A system integration test resolves the question of integrating system elements.
Every system element must have an integration test,
but an integration test must have more than once element to be a valid
integration test.
