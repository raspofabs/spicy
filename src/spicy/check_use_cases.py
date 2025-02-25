"""Check requirements for a TDP."""

import sys
from pathlib import Path
from typing import Callable, List, Optional

import click

from .use_cases import UseCase, gather_use_cases


def get_use_case_files(root_path: Optional[Path] = None) -> List[Path]:
    """Fetch a list of all the use-case files under a root path."""
    glob_root = root_path or Path("src/03_use_cases")
    if glob_root.is_file():
        return [glob_root]
    return sorted(glob_root.glob("*.md"))


def get_use_cases_from_files(file_paths: List[Path]) -> List[UseCase]:
    """Return the combined use cases from all the md files."""
    use_cases: List[UseCase] = []

    for filename in file_paths:
        use_cases.extend(gather_use_cases(filename))
    return use_cases


def render_issues(use_cases: List[UseCase], render_function: Optional[Callable] = None):
    """Render unresolved issues for each use-case."""
    render_function = render_function or print
    any_errors = False
    for use_case in use_cases:
        if use_case.render_issues():
            any_errors = True
    if not any_errors:
        render_function("No issues found.")
    return any_errors


@click.command()
@click.argument("path-override", required=False, default=None, type=Path)
def run(
    path_override: Optional[Path],
):
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
