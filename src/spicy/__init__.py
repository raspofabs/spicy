"""Spicy is like needs, but for mdbook."""

import sys
from functools import partial
from pathlib import Path
from typing import Any, Callable, List, Optional

import click

from .spec import SpecElement, get_specs_from_files
from .spec.builder import (
    SoftwareComponent,
    SoftwareRequirement,
    StakeholderNeed,
    StakeholderRequirement,
    SystemElement,
    SystemRequirement,
)
from .use_cases import UseCase, get_use_cases_from_files


def get_spec_files(root_path: Optional[Path] = None) -> List[Path]:
    """Fetch a list of all the use-case files under a root path."""
    glob_root = root_path or Path("src/")
    if glob_root.is_file():
        return [glob_root]
    return sorted(glob_root.glob("**/*.md"))


def render_issues(specs: List[SpecElement], use_cases: List[UseCase], render_function: Optional[Callable] = None):
    """Render unresolved issues for each use-case."""
    render_function = render_function or print
    any_errors = False
    for spec in specs:
        if spec.render_issues(render_function):
            any_errors = True
    for use_case in use_cases:
        if use_case.render_issues(render_function):
            any_errors = True
    if not any_errors:
        render_function("No issues found.")

    def just(checked_class: Any):
        return partial(filter, lambda x: isinstance(x, checked_class))

    # check all use cases are connected to at least one stakeholder need
    stakeholder_needs = list(just(StakeholderNeed)(specs))
    print(f"Have {len(stakeholder_needs)} stakeholder needs")
    # check all stakeholder needs are refined into at least one stakeholder requirements
    stakeholder_reqs = list(just(StakeholderRequirement)(specs))
    print(f"Have {len(stakeholder_reqs)} stakeholder requirements")
    # check all stakeholder requirements are fulfilled by at least one system requirement
    system_reqs = list(just(SystemRequirement)(specs))
    print(f"Have {len(system_reqs)} system requirements")
    # check all system requirements are captured by at least one system element
    system_elements = list(just(SystemElement)(specs))
    print(f"Have {len(system_elements)} system elements")
    # check all system elements which are software elements derive to at least one software requirement
    software_requirements = list(just(SoftwareRequirement)(specs))
    print(f"Have {len(software_requirements)} software requirements")
    # check all software requirements are satisfied by at least one software component
    software_components = list(just(SoftwareComponent)(specs))
    print(f"Have {len(software_components)} software components")
    # check all software components have at least one software unit design
    # check all software units have at least one unit test
    # check all software components have integration tests
    # check all software requiremnets have qualification tests
    # check all system elements have integration tests
    # check all system requirements have system qualification tests

    # bidirectional traceability does not require that all elements are
    # bi-directionally dependent, only that any stakeholder needs must be
    # traceable back and forth. Additional tests, software components, even
    # software requirements, can be introduced with rationale not originating
    # from the stakeholder needs.

    return any_errors


@click.command()
@click.argument("project-prefix", required=True, type=str)
@click.argument("path-override", required=False, default=None, type=Path)
def run(
    project_prefix: str,
    path_override: Optional[Path],
):
    """Find paths to read, then print out the TCLs of all the use-cases."""
    if path_override is not None:
        filenames = get_spec_files(path_override)
    else:
        filenames = get_spec_files()

    print(f"Have {len(filenames)} files to read.")
    specs = get_specs_from_files(project_prefix, filenames)
    use_cases = get_use_cases_from_files(filenames)
    for spec in specs:
        print(f"{spec.name} - {spec.spec_type}")
    print(f"Have {len(specs)} specs.")
    if render_issues(specs, use_cases):
        sys.exit(1)


if __name__ == "__main__":
    run()
