"""Check requirements for a TDP."""

import logging
import sys
from collections.abc import Callable
from pathlib import Path

import click

from .use_cases import UseCase, get_use_cases_from_files


def get_use_case_files(root_path: Path | None = None) -> list[Path]:
    """Fetch a list of all the use-case files under a root path."""
    glob_root = root_path or Path("src/03_use_cases")
    if glob_root.is_file():
        return [glob_root]
    return sorted(glob_root.glob("*.md"))


def render_issues(use_cases: list[UseCase], render_function: Callable | None = None):
    """Render unresolved issues for each use-case."""
    render_function = render_function or print
    any_errors = False
    for use_case in use_cases:
        if use_case.render_issues(render_function):
            any_errors = True
    if not any_errors:
        render_function("No issues found.")
    return any_errors


@click.command()
@click.argument("path-override", required=False, default=None, type=Path)
def run(
    path_override: Path | None,
):
    """Run a use case check."""
    logging.basicConfig(level=logging.INFO)
    """Find paths to read, then print out the TCLs of all the use-cases."""
    if path_override is not None:
        filenames = get_use_case_files(path_override)
    else:
        filenames = get_use_case_files()

    use_cases = get_use_cases_from_files(filenames)
    if render_issues(use_cases):
        sys.exit(1)


if __name__ == "__main__":
    run()
