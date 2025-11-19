# Spicy

Built as a tool to try to automate the tracking of non-compliance when
attempting to follow an ASPICE process.
Spicy tries to help by letting you know where there are missing documents,
missing links, and missing fields in your documentation.


# Installation

```sh
uv tool install . -e
```

# Operation

Tool configuration is minimal.
Either supply the project prefix on the command line or
provide a `.spicy.yaml` config file.

```sh
# with prefix
spicy --prefix PRJPREF docs/path

# with a docs/path/.spicy.yaml
spicy docs/path
```

The configuration file's only mandatory field is the prefix.
Examples can be found in the test data, but also in the Spicy
docs directory.

```yaml
----
prefix: PROJ
ignored_refs: # ignore references to things that aren't actually specs
  - PROJ_ENV_VAR
  - PROJ_VAL_TEST_.* # use regular expressions
ignored_links:
  SoftwareUnitTest:
    - Tests SoftwareUnit # we can ingore specific links
ignored_dependencies:
  SoftwareUnit:
    - SoftareUnitTest Tests # we can ignore specific dependencies
```
