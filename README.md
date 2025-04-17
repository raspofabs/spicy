# Spicy

Built as a tool to try to automate the tracking of non-compliance when
attempting to follow an ASPICE process.
Spicy tries to help by letting you know where there are missing documents,
missing links, and missing fields in your documentation.


# Installation

uv tool install . -e

# Operation

Tool configuration is minimal.
Either supply the project prefix on the command line or
provide a `.spicy.yaml` config file.

The configuration is currently only the prefix.
Examples can be found in the test data, but also in the Spicy
docs directory.

```yaml
prefix: PROJ
```
