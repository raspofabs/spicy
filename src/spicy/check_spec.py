"""Spicy is like needs, but for mdbook."""

import logging
import sys
from pathlib import Path

import click

from .render_spec_issues import render_issues
from .spec import get_specs_from_files
from .use_cases import get_use_cases_from_files

logger = logging.getLogger(__name__)


def get_spec_files(root_path: Path | None = None) -> list[Path]:
    """Fetch a list of all the use-case files under a root path."""
    glob_root = root_path or Path("src/")
    if glob_root.is_file():
        return [glob_root]
    return sorted(glob_root.glob("**/*.md"))


@click.command()
@click.argument("project-prefix", required=True, type=str)
@click.argument("path-override", required=False, default=None, type=Path)
def run(
    project_prefix: str,
    path_override: Path | None,
) -> None:
    """Find paths to read, then print out the TCLs of all the use-cases."""
    logging.basicConfig(level=logging.INFO)

    filenames = get_spec_files(path_override)

    logger.info("Found %s files to read.", len(filenames))
    specs = get_specs_from_files(project_prefix, filenames)
    use_cases = get_use_cases_from_files(filenames)
    logger.info("Discovered %s spec elements.", len(specs))
    if render_issues(specs, use_cases):
        sys.exit(1)


if __name__ == "__main__":
    run()
