"""Collecting use case data from a file or directory."""

from pathlib import Path
from typing import List

from spicy.md_read import load_syntax_tree

from .builder import UseCaseBuilder
from .use_case import UseCase


def gather_use_cases(from_file: Path) -> List[UseCase]:
    """Use markdown-it to get all the elements of the markdown files in the project."""
    node = load_syntax_tree(from_file)
    return UseCaseBuilder._parse_syntax_tree_to_use_cases(node, from_file)
