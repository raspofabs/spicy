"""Render use case issues to help with Tool Qualification."""
# pragma: exclude file

from collections.abc import Callable

from .use_cases.use_case import UseCase


def render_issues(use_cases: list[UseCase], render_function: Callable[[str], None] | None = None) -> bool:
    """Render unresolved issues for each use-case."""
    render_function = render_function or print
    any_errors = False
    for use_case in use_cases:
        issues = use_case.get_issues()
        if not issues:
            continue
        first_issue, *other_issues = issues
        render_function(first_issue)
        for issue in other_issues:
            render_function("\t" + issue)
        any_errors = True
    if not any_errors:
        render_function("No issues found.")
    return any_errors
