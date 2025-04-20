"""Spicy is like needs, but for mdbook."""

import logging
import sys
from pathlib import Path

import click

from .config import load_spicy_config
from .gather import get_elements_from_files, render_issues_with_elements

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
    if render_issues_with_elements(elements, print):
        sys.exit(1)
    logger.info("No issues found with spec")
