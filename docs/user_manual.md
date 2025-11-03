# User manual

Spicy is a command line tool that operates against command line parameters or a
local config file.
The options for spicy are whether to check the markdown links, fix any broken
links, or overrides for where to check and what the project prefix is.

```txt
Usage: spicy [OPTIONS] [PATH_OVERRIDE]

  Parse and analyze markdown spec files, optionally checking and/or fixing
  reference links.

  By default, runs in analysis mode only. Use --check-refs to check for broken
  or incorrect markdown reference links, and --fix-refs to update files in-
  place with correct links.

Options:
  -p, --project-prefix TEXT  Set the project prefix.
  -v, --verbose              Run in verbose mode.
  --fix-refs                 Fix markdown reference links in-place after
                             parsing (overwrites files).
  --check-refs               Check for correct markdown reference links in
                             content and report issues.
  --help                     Show this message and exit.
```

The config file has a few operational fields.
One is mandatory, the others are optional.

```yaml
---
prefix: PRE
ignored_refs:
  - PRE_ENV_VAR
  - PRE_.*_TEST_.*
ignored_links:
  SoftwareUnit:
    - Implements SoftwareComponent
  SoftwareArchitecture:
    - Fulfils SoftwareRequirement
ignored_dependencies:
  SoftwareArchitecture:
    - SoftwareComponent Implements
  SoftwareComponent:
    - SoftwareUnit Implements
  SoftwareUnit:
    - SoftwareUnitTest Tests
```

Ignored links can be useful to quieten the output
while the spec is being developed.
A spec cannot be considered complete until
the ignored links section is empty and spicy finds no issues.
