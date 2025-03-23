# Identify the products and processes

- Products: 
    - the tools and user documents,
    - hardware and software artefacts,
    - databases, services and credentials, and
    - any other deliverables to meet the stakeholder needs.
- Processes: 
    - how to configure the products for use as an integrator or installer of the product,
    - how to use the tools effectively,
    - how to verify the configuration, and
    - how to release the product.

### Interface requirements specification

- Define relationships between products, processes or process tasks
- Defines criteria and format for what is common to both
- Defines critical timing dependencies or sequence ordering
- Description of the physical interfaces of each system component like
    - bus interfaces (CAN, MOST, LIN, Flexray etc.)
    - transceiver (type, manufacturer, etc.)
    - analogue Interfaces
    - digital Interfaces (PWM, etc.)
    - additional Interfaces (IEEE, ISO, Bluetooth, USB, etc.
- Identification of the software interfaces of software components and other
  software item in terms of
    - inter-process communication mechanisms
    - bus communication mechanisms


## Static aspects of the system

- description of the components making up the system
- locations of elements
- interfaces between the elements
- supported inputs
- expected outputs

## Dymamic aspects of the system

- version management of the elements
- sequential coupling between elements
- storage of violations
- reviewing changes in violations
- storage of historical data

## Phases

- Introduction of the tooling.
- General usage of the tooling.
- Winding down and obsolescence.

## Deployment

- How the tool should be installed and deployed.
- How and when the tool version is checked.

## Alternative solutions

Alternative solutions should be presented.

- Open source and close source or "COTS" solutions.
- Partial solutions working together.
- Reuse or evolution of existing tools.

Consider:

- Why are none of the existing options applicable?
- Which stakeholder needs or requirements are not met by those solutions?
- Why can't those missing requirements able to be added to existing solutions?
