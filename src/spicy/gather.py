"""Collecting spec data from a file or directory."""

import logging
import os
import re
from collections.abc import Callable
from pathlib import Path

from spicy.md_read import load_syntax_tree, strip_link

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

    # Always build expected_links for all elements
    build_expected_links(specs)

    return specs


def build_expected_links(elements: list[SpecElement]) -> None:
    """Populate each SpecElement with an expected_links dict for each link field."""
    lookup = {}
    for el in elements:
        lookup[(el.variant, el.name)] = el.file_path

    def anchorify(text: str) -> str:
        anchor = text.strip().lower().replace(" ", "-").replace("_", "-")
        anchor = re.sub(r"[^a-z0-9\-]", "", anchor)
        anchor = re.sub(r"-+", "-", anchor)
        return anchor.strip("-")

    for el in elements:
        expected_links: dict[str, list[tuple[str, str]]] = {}
        required_links = expected_links_for_variant(el.variant)
        for link, _ in required_links:
            link_key = section_name_to_key(link) or link
            expected_links[link_key] = []
            if link_key in el.content:
                for target in el.content[link_key]:
                    target_text = strip_link(target)
                    found = None
                    for (v, n), path in lookup.items():
                        if n == target_text:
                            found = (v, n, path)
                            break
                    if found:
                        _, _, target_path = found
                        rel_path = os.path.relpath(target_path, el.file_path.parent)
                        anchor = anchorify(target_text)
                        md_link = f"[{target_text}]({rel_path}#{anchor})"
                        expected_links[link_key].append((target_text, md_link))
        el.expected_links = expected_links
