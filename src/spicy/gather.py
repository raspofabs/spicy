"""Collecting spec data from a file or directory."""

import logging
from collections import Counter, defaultdict
from collections.abc import Callable
from pathlib import Path

from spicy.md_read import load_syntax_tree

from .parser import parse_syntax_tree_to_spec_elements
from .parser.spec_element import SpecElement
from .parser.spec_utils import (
    expected_backlinks_for_variant,
    expected_links_for_variant,
    expected_variants,
    section_name_to_key,
    spec_is_defined,
    spec_is_software,
)

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


SpecVariantMap = defaultdict[str, dict[str, SpecElement]]


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

    # prerequisite for this map is that all specs have unique names
    spec_variant_map: SpecVariantMap = defaultdict(dict)
    for spec in spec_elements:
        spec_variant_map[spec.variant][spec.name] = spec

    for variant in expected_variants():
        any_errors |= render_spec_linkage_issues(spec_variant_map, render_function, variant)

    return any_errors


def render_spec_linkage_issues(
    spec_variant_map: SpecVariantMap,
    render_function: RenderFunction,
    spec_type_to_inspect: str,
) -> bool:
    """Check all specs links are connected to real specs and any required backlinks are observed."""
    any_errors = False
    if not spec_is_defined(spec_type_to_inspect):  # pragma: no cover (only for code regression)
        msg = f"Spec type [{spec_type_to_inspect}] is not defined."
        raise AssertionError(msg)

    inspected_specs_map = spec_variant_map[spec_type_to_inspect]
    inspected_specs_names = set(inspected_specs_map.keys())
    if not inspected_specs_names:
        return False
    logger.debug(
        "Have %s spec of type %s (%s)",
        len(inspected_specs_map),
        spec_type_to_inspect,
        ", ".join(inspected_specs_names),
    )

    any_errors |= render_spec_simple_linkage_issues(spec_variant_map, render_function, spec_type_to_inspect)
    any_errors |= render_spec_back_linkage_issues(spec_variant_map, render_function, spec_type_to_inspect)

    return any_errors


def render_spec_simple_linkage_issues(
    spec_variant_map: SpecVariantMap,
    render_function: RenderFunction,
    spec_type_to_inspect: str,
) -> bool:
    """Check all specs links are connected to real specs and any required backlinks are observed."""
    any_errors = False

    inspected_specs_map = spec_variant_map[spec_type_to_inspect]

    for link, target in expected_links_for_variant(spec_type_to_inspect):
        link_key = section_name_to_key(link) or link
        target_specs_map = spec_variant_map[target]
        target_spec_names = set(target_specs_map.keys())
        logger.debug("Target spec names: %s", ", ".join(target_spec_names))

        for inspected_spec in inspected_specs_map.values():
            fulfilment = set(inspected_spec.get_linked_by(link_key))
            logger.debug("Fulfilment: %s", ", ".join(fulfilment))
            if disconnected := fulfilment - target_spec_names:
                any_errors = True
                disconnected_list = ", ".join(sorted(disconnected))
                render_function(
                    f"{spec_type_to_inspect} {inspected_spec.name} {link} unexpected {target} {disconnected_list}",
                )
    return any_errors


def render_spec_back_linkage_issues(
    spec_variant_map: SpecVariantMap,
    render_function: RenderFunction,
    spec_type_to_inspect: str,
) -> bool:
    """Check all specs links are connected to real specs and any required backlinks are observed."""
    any_errors = False

    inspected_specs_map = spec_variant_map[spec_type_to_inspect]

    for source, link in expected_backlinks_for_variant(spec_type_to_inspect):
        # unused is per link
        logger.debug("Checking backlinks: %s %s %s", source, link, spec_type_to_inspect)
        unused_target_specs = set(inspected_specs_map.keys())

        if spec_is_software(source):
            unused_target_specs = {name for name, spec in inspected_specs_map.items() if spec.is_software_element}

        link_key = section_name_to_key(link) or link
        source_specs_map = spec_variant_map[source]
        source_spec_names = set(source_specs_map.keys())
        logger.debug("Source spec names: %s", ", ".join(source_spec_names))

        for source_spec in source_specs_map.values():
            fulfilment = set(source_spec.get_linked_by(link_key))
            logger.debug("Source link: %s", ", ".join(fulfilment))
            unused_target_specs = unused_target_specs - fulfilment

        if unused_target_specs:
            any_errors = True
            render_function(f"{spec_type_to_inspect} without a {source}:")
            for unused_target in sorted(unused_target_specs):
                render_function(f"\t{unused_target}")

    return any_errors
