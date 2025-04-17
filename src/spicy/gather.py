"""Collecting spec data from a file or directory."""

from collections import Counter
from collections.abc import Callable
from pathlib import Path

from spicy.md_read import load_syntax_tree

from .parser import parse_syntax_tree_to_spec_elements
from .parser.spec_element import SpecElement


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
    render_function: Callable[[str], None] | None = None,
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
