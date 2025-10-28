"""Spicy is like needs, but for mdbook."""

import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import click

from .config import load_spicy_config
from .gather import get_elements_from_files
from .review import render_issues_with_elements

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
@click.option(
    "--fix-refs",
    "_fix_refs",
    is_flag=True,
    default=False,
    help="Fix markdown reference links in-place after parsing (overwrites files).",
)
@click.option(
    "--check-refs",
    "_check_refs",
    is_flag=True,
    default=False,
    help="Check for correct markdown reference links in content and report issues.",
)
def run(
    path_override: Path | None,
    project_prefix: str | None,
    verbose: bool,  # noqa: FBT001
    _fix_refs: bool,  # noqa: FBT001
    _check_refs: bool,  # noqa: FBT001
) -> None:
    """Parse and analyze markdown spec files, optionally checking and/or fixing reference links.

    By default, runs in analysis mode only.
    Use --check-refs to check for broken or incorrect markdown reference links,
    and --fix-refs to update files in-place with correct links.
    """
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

    render_function: Callable[[str], None] = print

    if render_issues_with_elements(
        elements,
        config=spicy_config,
        render_function=render_function,
    ):
        sys.exit(1)
    render_function(f"No issues found with any of the {len(elements)} specs")
