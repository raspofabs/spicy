"""Collecting spec data from a file or directory."""

import logging
from collections import Counter
from collections.abc import Callable
from pathlib import Path

from spicy.md_read import load_syntax_tree

from .parser import parse_syntax_tree_to_spec_elements
from .parser.spec_element import SpecElement
from .parser.spec_utils import expected_links_for_variant, section_name_to_key

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

    if not any_errors:
        render_function("No spec issues found.")
    return any_errors


def render_spec_linkage_issues(
    specs: list[SpecElement],
    render_function: RenderFunction,
    spec_type_to_inspect: str,
) -> bool:
    """Check all specs links are connected to real specs and any required backlinks are observed."""
    any_errors = False

    inspected_specs = [spec for spec in specs if spec.variant == spec_type_to_inspect]
    logger.debug("Have %s stakeholder needs", len(inspected_specs))

    inspected_specs_map = {n.name: n for n in inspected_specs}
    inspected_specs_names = set(inspected_specs_map.keys())
    unused_specs = set(inspected_specs_names)

    for link, target in expected_links_for_variant(spec_type_to_inspect):
        link_key = section_name_to_key(link) or link
        target_specs = [spec for spec in specs if spec.variant == target]
        target_spec_names = {n.name for n in target_specs}

        for inspected_spec in inspected_specs:
            fulfilment = set(inspected_spec.get_linked_by(link_key))
            if disconnected := fulfilment - target_spec_names:
                any_errors = True
                render_function(
                    f"{spec_type_to_inspect} {inspected_spec.name} {link} unexpected {target} {disconnected}",
                )
            unused_specs = unused_specs - fulfilment

    if unused_specs:
        any_errors = True
        render_function("Needs without a use-case:")
        for unused_need in sorted(unused_specs):
            render_function(f"\t{unused_need}")

    return any_errors
