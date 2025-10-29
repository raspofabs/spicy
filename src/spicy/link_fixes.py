"""Functions to automatically fix md link issues with a spec."""

import re
from pathlib import Path


def check_markdown_refs(file_list: list[Path], *, prefix: str, fix_refs: bool = False) -> int:
    """Check matching refs are correctly linked, optionally fixing them."""
    targets = {}
    re_section = get_section_pattern_from_prefix(prefix)
    for path in file_list:
        for target, line in get_targets_from_md(path.read_text(), re_section).items():
            targets[target] = (path, line)

    if fix_refs:
        pass

    return 0


def get_section_pattern_from_prefix(prefix: str) -> re.Pattern[str]:
    """Return a regular expression for use when capturing valid section headers."""
    return re.compile(rf"^#+ ({prefix}_\w+)$")


def get_targets_from_md(md_content: str, section_matcher: re.Pattern[str]) -> dict[str, int]:
    """Get a dictionary of targets to line numbers from a file."""
    targets: dict[str, int] = {}
    for line_number, text in enumerate(md_content.split("\n")):
        if m := section_matcher.match(text):
            targets[m.group(1)] = line_number
    return targets
