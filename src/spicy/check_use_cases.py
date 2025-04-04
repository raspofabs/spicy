"""Check requirements for a TDP."""

import logging
import sys
from pathlib import Path

import click

from .render_use_case_issues import render_issues
from .use_cases import get_use_cases_from_files


def get_use_case_files(root_path: Path | None = None) -> list[Path]:
    """Fetch a list of all the use-case files under a root path."""
    glob_root = root_path or Path("src/03_use_cases")
    if glob_root.is_file():
        return [glob_root]
    return sorted(glob_root.glob("*.md"))


@click.command()
@click.argument("path-override", required=False, default=None, type=Path)
def run(
    path_override: Path | None,
) -> None:
    """Find paths to read, then print out the TCLs of all the use-cases."""
    logging.basicConfig(level=logging.INFO)

    filenames = get_use_case_files(path_override)
    use_cases = get_use_cases_from_files(filenames)
    if render_issues(use_cases):
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    run()
