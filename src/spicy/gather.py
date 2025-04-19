"""Collecting spec data from a file or directory."""

import logging
from collections import Counter
from collections.abc import Callable
from pathlib import Path

from spicy.md_read import load_syntax_tree

from .parser import parse_syntax_tree_to_spec_elements
from .parser.spec_element import SpecElement
from .parser.spec_utils import expected_links_for_variant, section_name_to_key, spec_is_defined

logger = logging.getLogger(__name__)

RenderFunction = Callable[[str], None]


def gather_all_elements(project_prefix: str, from_file: Path) -> list[SpecElement]:
    """Use markdown-it to get all the elements of the markdown files in the project."""
    if from_file.is_dir():
        complete_list: list[SpecElement] = []
        for path in from_file.glob("**/*.md"):
            if path.is_file():
                complete_list.extend(gather_all_elements(project_prefix, path))
        return complete_list
    node = load_syntax_tree(from_file)
    return parse_syntax_tree_to_spec_elements(project_prefix, node, from_file)


def get_elements_from_files(project_prefix: str, file_paths: list[Path]) -> list[SpecElement]:
    """Return the combined use cases from all the md files."""
    specs: list[SpecElement] = []

    for filename in file_paths:
        specs.extend(gather_all_elements(project_prefix, filename))
    return specs


def render_issues_with_elements(
    spec_elements: list[SpecElement],
    render_function: RenderFunction | None = None,
) -> bool:
    """Render unresolved issues for each Spec Element."""
    render_function = render_function or print
    if not spec_elements:
        render_function("No elements.")
        return True
    any_errors = False
    # check for non-unique specs
    for spec_name, count in Counter(x.name for x in spec_elements).items():
        if count > 1:
            render_function(f"Non unique name {spec_name} has {count} instances")
    # check each spec for any issues
    for spec in spec_elements:
        for issue in spec.get_issues():
            render_function(issue)
            any_errors = True

    # Tool Qualification: UseCase
    any_errors |= render_spec_linkage_issues(spec_elements, render_function, "UseCase")

    # SYS.1: StakeholderNeeds
    any_errors |= render_spec_linkage_issues(spec_elements, render_function, "StakeholderNeed")

    # SYS.1: StakeholderRequirements
    any_errors |= render_spec_linkage_issues(spec_elements, render_function, "StakeholderRequirement")

    # SYS.2: SystemRequirements
    any_errors |= render_spec_linkage_issues(spec_elements, render_function, "SystemRequirement")

    # SYS.3: SystemElements
    any_errors |= render_spec_linkage_issues(spec_elements, render_function, "SystemElement")

    # SWE.1: SoftwareRequirements
    any_errors |= render_spec_linkage_issues(spec_elements, render_function, "SoftwareRequirement")

    # SWE.2: SoftwareComponents
    any_errors |= render_spec_linkage_issues(spec_elements, render_function, "SoftwareComponent")

    # SWE.3: SoftwareUnits
    any_errors |= render_spec_linkage_issues(spec_elements, render_function, "SoftwareUnit")

    # SWE.5: SoftwareIntegration
    any_errors |= render_spec_linkage_issues(spec_elements, render_function, "SoftwareIntegration")

    # SWE.6: SoftwareQualification
    any_errors |= render_spec_linkage_issues(spec_elements, render_function, "SoftwareQualification")

    # SYS.4: SystemIntegration
    any_errors |= render_spec_linkage_issues(spec_elements, render_function, "SystemIntegration")

    # SYS.5: SystemQualification
    any_errors |= render_spec_linkage_issues(spec_elements, render_function, "SystemQualification")

    # VAL.1: Validation
    any_errors |= render_spec_linkage_issues(spec_elements, render_function, "Validation")

    return any_errors


def render_spec_linkage_issues(
    specs: list[SpecElement],
    render_function: RenderFunction,
    spec_type_to_inspect: str,
) -> bool:
    """Check all specs links are connected to real specs and any required backlinks are observed."""
    any_errors = False
    if not spec_is_defined(spec_type_to_inspect):  # pragma: no cover (only for code regression)
        msg = f"Spec type [{spec_type_to_inspect}] is not defined."
        raise AssertionError(msg)

    inspected_specs = [spec for spec in specs if spec.variant == spec_type_to_inspect]

    inspected_specs_map = {n.name: n for n in inspected_specs}
    inspected_specs_names = set(inspected_specs_map.keys())
    logger.debug(
        "Have %s spec of type %s (%s)",
        len(inspected_specs),
        spec_type_to_inspect,
        ", ".join(inspected_specs_names),
    )

    for link, target in expected_links_for_variant(spec_type_to_inspect):
        unused_specs = set(inspected_specs_names)

        link_key = section_name_to_key(link) or link
        target_specs = [spec for spec in specs if spec.variant == target]
        target_spec_names = {n.name for n in target_specs}
        logger.debug("Target spec names: %s", ", ".join(target_spec_names))

        for inspected_spec in inspected_specs:
            fulfilment = set(inspected_spec.get_linked_by(link_key))
            logger.debug("Fulfilment: %s", ", ".join(fulfilment))
            if disconnected := fulfilment - target_spec_names:
                any_errors = True
                disconnected_list = ", ".join(disconnected)
                render_function(
                    f"{spec_type_to_inspect} {inspected_spec.name} {link} unexpected {target} {disconnected_list}",
                )
            unused_specs = unused_specs - fulfilment

        if unused_specs:
            any_errors = True
            render_function(f"{spec_type_to_inspect} without a {target}:")
            for unused_need in sorted(unused_specs):
                render_function(f"\t{unused_need}")

    return any_errors
