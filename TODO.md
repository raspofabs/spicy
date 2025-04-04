# task list

- Rename TDP stuff (that's a work naming convention. ISO-26262 calls it the tool qualification plan)
- Move to spicy config controlling more stuff
    - which specs exist
    - how they are linked
    - what their requirements are:
        - must be linked,
        - must have at least N links
        - must be linked to something matching a specific filter
        - these rules also apply behind a filter
            - e.g. if the spec is a safety/security requirement, then it should be fulfilled by at least one safety/security implementation spec
