"""Collecting use case data from a file or directory."""
# pragma: exclude file

from pathlib import Path

from spicy.md_read import load_syntax_tree

from .builder import parse_syntax_tree_to_use_cases
from .use_case import UseCase


def gather_use_cases(from_file: Path) -> list[UseCase]:
    """Use markdown-it to get all the elements of the markdown files in the project."""
    node = load_syntax_tree(from_file)
    return parse_syntax_tree_to_use_cases(node, from_file)


def get_use_cases_from_files(file_paths: list[Path]) -> list[UseCase]:
    """Return the combined use cases from all the md files."""
    use_cases: list[UseCase] = []

    for filename in file_paths:
        use_cases.extend(gather_use_cases(filename))
    return use_cases
