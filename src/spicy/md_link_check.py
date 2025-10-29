"""Functions to automatically fix md link issues with a spec."""

import re
from pathlib import Path


def check_markdown_refs(file_list: list[Path], *, base_path: Path, prefix: str, fix_refs: bool = False) -> list[str]:
    """Check matching refs are correctly linked, optionally fixing them."""
    targets = {}
    references = {}
    re_section = get_section_pattern_from_prefix(prefix)
    re_reference = get_section_reference_pattern_from_prefix(prefix)

    for path in file_list:
        content = path.read_text()
        for target, line in get_matches_from_md(content, re_section).items():
            targets[target] = (path, line)
        for reference, line in get_matches_from_md(content, re_reference).items():
            # skip any that are actually sections
            if (path, line) in targets.values():
                continue
            references[reference] = (path, line)

    expected_targets = {
        target: f"[{target}]({path.relative_to(base_path)}#{target.lower()})" for target, (path, _) in targets.items()
    }

    issue_list = []
    # check for completely invalid references
    for ref, (path, line) in references.items():
        if ref not in targets:
            issue_list.append(f"Bad reference found: {ref} in {path}({line}) has no matching section.")
        else:
            line_content = path.read_text().split("\n")[line]
            re_link = get_link_pattern_from_reference(ref)
            m = re_link.search(line_content)
            # check that all references have links
            if not m:
                issue_list.append(f"Reference without a link: {ref} in {path}({line})")
                continue
            expected = expected_targets[ref]
            actual = m.group(1)
            # check that all links are correct
            if expected != actual:
                # or update if fix_refs is True
                if fix_refs:
                    path.write_text(path.read_text().replace(actual, expected))
                else:
                    issue_list.append(
                        f"Reference has bad link: {ref} in {path}({line}) is {actual} but should be {expected}",
                    )
    return issue_list


def get_section_pattern_from_prefix(prefix: str) -> re.Pattern[str]:
    """Return a regular expression for use when capturing valid section headers."""
    return re.compile(rf"^#+ ({prefix}_\w+)$")


def get_section_reference_pattern_from_prefix(prefix: str) -> re.Pattern[str]:
    """Return a regular expression for use when capturing section references."""
    return re.compile(rf"(\b{prefix}_\w+\b)")


def get_link_pattern_from_reference(reference: str) -> re.Pattern[str]:
    """Return a regular expression for use when capturing section references."""
    return re.compile(rf"(\[{reference}\]\([\w\./#]+\))")


def get_matches_from_md(md_content: str, section_matcher: re.Pattern[str]) -> dict[str, int]:
    """Get a dictionary of targets to line numbers from a file."""
    targets: dict[str, int] = {}
    for line_number, text in enumerate(md_content.split("\n")):
        for m in section_matcher.finditer(text):
            targets[m.group(1)] = line_number
    return targets
