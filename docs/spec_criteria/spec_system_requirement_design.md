# Steps:

1. Identify and document the functional and non-functional requirements from
   stakeholder requirements.
   System requirements are written from the perspective of the technical system
   but still fulfil the stakeholder's needs.
2. Analyse the impact of the architecture on the system context (operating
   environment).

# System requirements specification

- System requirements include:
    - functions and capabilities of the system;
    - business, organizational and user requirements;
    - safety, security, human-factors engineering (ergonomics), interface,
      operations, and maintenance requirements;
    - design constraints and qualification requirements.
    - Source: (ISO/IEC 12207)
- Identifies the required system overview
- Identifies any interrelationship considerations / constraints between system elements
- Identifies any relationship considerations / constraints between the system elements and the software
- Identifies any design considerations / constraints for each required system element, including:
    - memory / capacity requirements
    - hardware interfaces requirements
    - user interfaces requirements
    - external system interface requirements
    - performance requirements
    - commands structures
    - security / data protection characteristics
    - application parameter settings
    - manual operations
    - reusable components
- Describes the operation capabilities
- Describes environmental capabilities
- Documentation requirements
- Reliability requirements
- Logistical Requirements
- Describes security requirements
- Diagnosis requirements

## Business Requirements:

Such as requirement to achieve certain compliance level.
They are about what the system will need to do to resolve some lack in
what the business is capable of.
Think in terms of KPIs and goals.
These needs are likely to be less strict, easily prioritised, even optional.

## Organizational requirements:

These can be things like the limit on the cost to deliver or the
availability of the implmementors or verifiers.
Constraints can include how and when the system works with existing processes.
Limitations can include the working environment and tools available.

## User requirement:

Requirements related to the users, such as their skills and strengths, weaknesses or deficiencies.
Requirements for the effectiveness of the solution system in terms of performance and maintainability.

## Safety and security requirements:

Related to safety and security.

## Human-factors engineering (ergonomics):

Relates to the way which the system is used by humans.

## Interface requirements:

what affordances it must have to external systems, e.g. document formats for delivery.

## Operations requirements:

Operations is about the running of the system.
These requirements can be about uptime, time to recovery, or updating procedures.
They can relate to logs, and the ability to rollback changes.
Observability might exist here.
Documentation on how to fix issues would be an operational requirement.
For some tools, it can include how to integrate into the existing infrastructure.

## Maintenance requirements:

Possibly the simplest of the requirements to describe.
What restrictions must there be, such as what are the minimum acceptable times
between failure, and servicing.
What is the skill limit on those who will be carrying out the maintenance.
What restrictions on how the system is updated and rolled-back in case of
issues.
What information must be available in reports or dashboards on the state of the
system?

## Design requirements:

These are requirements generally about the structure or implementation.
They can include decisions to use specific architectures, frameworks,
or approaches to resolving other problems or requirements.

## Qualification requirements:

Define the features that define whether the system is able to do its job
Characteristics, attributes, or properties of the system that must be
present, otherwise the system is not fit for purpose.
Examples include operational limits such as storage space,
temperature, or qualification measures such as whether it meets the
constraints of a development process of international standards
document for code-quality.

# Verification Criteria

- Each requirement is verifiable or can be assessed
- Verification criteria define the qualitative and quantitative criteria for
  verification of a requirement.
- Verification criteria demonstrate that a requirement can be verified within
  agreed constraints. (Additional Requirement to 17-00 Requirements
  specification)

# Spec in the document

This is how we want to see the spec:

```md
Specification:

- **Requirement type:**
  - business function, organisational function;
  - user, safety, security, ergonomic, interface;
  - operational, maintenance;
  - design constraint;
  - qualification
- **Interaction:** system elements / software, nature of interaction
- **Constraints:** resource limits; performance constraints; safety, security expectations; interface and API constraints
- **Operational and environmental limits and capabilities:**
- **Documentation:** where it is, what it is for.
- **Qualification relevant:** yes/no
- **Auditable:** yes/no
```


# Beyond this:

- Identifies any relationship considerations / constraints between the system elements and the software
- Identifies any interrelationship considerations / constraints between system elements
- Identifies the required system overview
- Identifies any design considerations / constraints for each required system element, including:
    - memory / capacity requirements
    - hardware interfaces requirements
    - user interfaces requirements
    - external system interface requirements
    - performance requirements
    - commands structures
    - security / data protection characteristics
    - application parameter settings
    - manual operations
    - reusable components
- Describes the operation capabilities
- Describes environmental capabilities
- Documentation requirements
- Reliability requirements
- Logistical Requirements
- Describes security requirements
- Diagnosis requirements
