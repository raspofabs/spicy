"""Collecting spec data from a file or directory."""

from pathlib import Path

from spicy.md_read import load_syntax_tree

from .builder import SpecElementBuilder
from .spec_element_base import SpecElementBase


def gather_spec_elements(project_prefix: str, from_file: Path) -> list[SpecElementBase]:
    """Use markdown-it to get all the elements of the markdown files in the project."""
    if from_file.is_dir():
        complete_list = []
        for path in from_file.glob("**/*.md"):
            if path.is_file():
                complete_list.extend(gather_spec_elements(project_prefix, path))
        return complete_list
    node = load_syntax_tree(from_file)
    return SpecElementBuilder.parse_syntax_tree_to_spec_elements(project_prefix, node, from_file)


def get_specs_from_files(project_prefix: str, file_paths: list[Path]) -> list[SpecElementBase]:
    """Return the combined use cases from all the md files."""
    specs: list[SpecElementBase] = []

    for filename in file_paths:
        specs.extend(gather_spec_elements(project_prefix, filename))
    return specs


def get_elements_from_files(project_prefix: str, file_paths: list[Path]) -> list[SpecElementBase]:
    """Return the combined use cases from all the md files."""
    specs: list[SpecElementBase] = []

    for filename in file_paths:
        specs.extend(gather_spec_elements(project_prefix, filename))
    return specs
