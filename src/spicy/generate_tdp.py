"""Create a TDP from the documentation."""
# pragma: exclude file

import logging
import sys
from pathlib import Path

import click

from .use_cases import UseCase, gather_use_cases


def get_use_case_files(root_path: Path | None = None) -> list[Path]:
    """Fetch a list of all the use-case files under a root path."""
    glob_root = root_path or Path("src/03_use_cases")
    if glob_root.is_file():
        return [glob_root]
    return sorted(glob_root.glob("*.md"))


def get_use_cases_from_files(file_paths: list[Path]) -> list[UseCase]:
    """Return the combined use cases from all the md files."""
    use_cases: list[UseCase] = []

    for filename in file_paths:
        use_cases.extend(gather_use_cases(filename))
    return use_cases


def render_issues(use_cases: list[UseCase]) -> bool:
    """Render unresolved issues for each use-case."""
    any_errors = False
    for use_case in use_cases:
        issues = use_case.get_issues()
        if not issues:
            continue
        first_issue, *other_issues = issues
        print(first_issue)  # noqa: T201
        for issue in other_issues:
            print("\t" + issue)  # noqa: T201
        any_errors = True
    return any_errors


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


if __name__ == "__main__":
    run()
