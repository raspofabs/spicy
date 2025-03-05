"""Spicy is like needs, but for mdbook."""

import sys
from pathlib import Path
from typing import Callable, List, Optional

import click

from .spec import SpecElement, get_specs_from_files
from .use_cases import get_use_cases_from_files


def get_spec_files(root_path: Optional[Path] = None) -> List[Path]:
    """Fetch a list of all the use-case files under a root path."""
    glob_root = root_path or Path("src/")
    if glob_root.is_file():
        return [glob_root]
    return sorted(glob_root.glob("**/*.md"))


def render_issues(specs: List[SpecElement], render_function: Optional[Callable] = None):
    """Render unresolved issues for each use-case."""
    render_function = render_function or print
    any_errors = False
    for spec in specs:
        if spec.render_issues():
            any_errors = True
    if not any_errors:
        render_function("No issues found.")
    return any_errors


@click.command()
@click.argument("project-prefix", required=True, type=str)
@click.argument("path-override", required=False, default=None, type=Path)
def run(
    project_prefix: str,
    path_override: Optional[Path],
):
    """Find paths to read, then print out the TCLs of all the use-cases."""
    if path_override is not None:
        filenames = get_spec_files(path_override)
    else:
        filenames = get_spec_files()

    print(f"Have {len(filenames)} files to read.")
    specs = get_specs_from_files(project_prefix, filenames)
    use_cases = get_use_cases_from_files(filenames)
    for spec in specs:
        print(f"{spec.name} - {spec.spec_type}")
    print(f"Have {len(specs)} specs.")
    if render_issues(specs):
        sys.exit(1)


if __name__ == "__main__":
    run()
