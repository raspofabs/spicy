"""Spicy is like needs, but for mdbook."""

import logging
import sys
from pathlib import Path

import click

from .config import load_spicy_config
from .render_spec_issues import render_issues, render_issues_with_elements
from .spec import get_elements_from_files, get_specs_from_files
from .use_cases import get_use_cases_from_files

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
def run(
    path_override: Path | None,
    project_prefix: str | None,
) -> None:
    """Find paths to read, then print out the TCLs of all the use-cases."""
    spicy_config = load_spicy_config(path_override or Path(), prefix=project_prefix)

    project_prefix = spicy_config.get("prefix")

    if project_prefix is None:
        logger.error("Unable to scan without a known prefix")
        sys.exit(1)

    logging.basicConfig(level=logging.INFO)

    filenames = get_spec_files(path_override)

    logger.info("Found %s files to read.", len(filenames))
    specs = get_specs_from_files(project_prefix, filenames)
    use_cases = get_use_cases_from_files(filenames)
    logger.info("Discovered %s spec elements.", len(specs))
    if render_issues(specs, use_cases):
        sys.exit(1)

    elements = get_elements_from_files(project_prefix, filenames)
    if render_issues_with_elements(elements):
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    run()
