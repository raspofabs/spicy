"""Spicy is like needs, but for mdbook."""

import logging
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import click

from .config import load_spicy_config
from .gather import get_elements_from_files, render_issues_with_elements
from .parser.spec_utils import expected_links_for_variant, section_name_to_key


def add_markdown_links_to_elements(elements: list) -> None:
    """Update link fields in SpecElements to be proper markdown links with relative paths."""
    # Build lookup: (variant, name) -> file_path
    lookup = {}
    for el in elements:
        lookup[(el.variant, el.name)] = el.file_path

    import re

    def anchorify(text: str) -> str:
        # Lowercase, replace spaces/underscores with dashes, remove non-alphanum/dash
        anchor = text.strip().lower().replace(" ", "-").replace("_", "-")
        anchor = re.sub(r"[^a-z0-9\-]", "", anchor)
        anchor = re.sub(r"-+", "-", anchor)
        return anchor.strip("-")

    for el in elements:
        required_links = expected_links_for_variant(el.variant)
        for link, _ in required_links:
            link_key = section_name_to_key(link) or link
            if link_key in el.content:
                new_links = []
                for target in el.content[link_key]:
                    found = None
                    for (v, n), path in lookup.items():
                        if n == target:
                            found = (v, n, path)
                            break
                    if found:
                        _, _, target_path = found
                        rel_path = os.path.relpath(target_path, el.file_path.parent)
                        anchor = anchorify(target)
                        md_link = f"[{target}]({rel_path}#{anchor})"
                        new_links.append(md_link)
                    else:
                        new_links.append(target)
                el.content[link_key] = new_links


if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

logger = logging.getLogger(__name__)


def get_spec_files(root_path: Path | None = None) -> list[Path]:
    """Fetch a list of all the use-case files under a root path."""
    glob_root = root_path or Path("src/")
    if glob_root.is_file():
        return [glob_root]
    return sorted(glob_root.glob("**/*.md"))


@click.command()
@click.argument("path-override", required=False, default=None, type=Path)
@click.option("-p", "--project-prefix", default=None, type=str, help="Set the project prefix.")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Run in verbose mode.")
def run(
    path_override: Path | None,
    project_prefix: str | None,
    verbose: bool,  # noqa: FBT001
) -> None:
    """Find paths to read, then print out the TCLs of all the use-cases."""
    spicy_config = load_spicy_config(path_override or Path(), prefix=project_prefix)

    if verbose:
        logger.setLevel(logging.DEBUG)

    project_prefix = spicy_config.get("prefix")

    if project_prefix is None:
        logger.error("Unable to scan without a known prefix")
        sys.exit(1)

    logging.basicConfig(level=logging.INFO)

    filenames = get_spec_files(path_override)

    logger.debug("Found %s files to read.", len(filenames))
    elements = get_elements_from_files(project_prefix, filenames)

    logger.debug("Discovered %s elements.", len(elements))

    # Add markdown links to elements
    add_markdown_links_to_elements(elements)

    render_function: Callable[[str], None] = print

    if render_issues_with_elements(elements, render_function):
        sys.exit(1)
    render_function(f"No issues found with any of the {len(elements)} specs")
