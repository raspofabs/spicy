# task list

- Better link fixing:
    - If the link is valid, but suboptimal, keep it. (example: uses absolute, but could be shorter if relative)
        - maybe only do this if the relative is in a subdirectory.
    - ignore refs in code or comments
- Move to spicy config controlling more stuff
    - which specs exist
    - how they are linked
    - what their requirements are:
        - must be linked,
        - must have at least N links
        - must be linked to something matching a specific filter
        - these rules also apply behind a filter
            - e.g. if the spec is a safety/security requirement, then it should be fulfilled by at least one safety/security implementation spec
