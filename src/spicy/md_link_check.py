"""Functions to automatically fix md link issues with a spec."""

import re
from collections import defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

TARGETS_DICT = dict[str, tuple[Path, int]]
REFS_DICT = defaultdict[str, list[tuple[Path, int]]]


@dataclass
class Edit:
    """Represent an edit to a file."""

    line: int
    actual: str
    replacement: str


def check_markdown_refs(
    file_list: list[Path],
    *,
    base_path: Path,
    prefix: str,
    fix_refs: bool,
    ignored_refs: list[str],
) -> list[str]:
    """Check matching refs are correctly linked, optionally fixing them."""
    targets, references = gather_markdown_sections_and_refs(file_list, prefix, ignored_refs)

    absolute_links = {
        target: f"[{target}](/{path.relative_to(base_path)}#{target.lower()})" for target, (path, _) in targets.items()
    }
    valid_targets = list(targets)

    issue_list = []

    edits: dict[Path, list[Edit]] = defaultdict(list)

    # check for completely invalid references
    for ref, list_of_locations in references.items():
        for path, line in list_of_locations:
            if ref not in targets:
                best_alternative = f"Did you mean {closest_string(ref, valid_targets)}"
                issue = f"Bad reference found: {ref} in {path}({line + 1}) has no matching section."
                issue_list.append(f"{issue} {best_alternative}")
            else:
                expected = f"[{ref}](#{ref.lower()})" if path == targets[ref][0] else absolute_links[ref]
                line_content = path.read_text().split("\n")[line]
                re_link = get_link_pattern_from_reference(ref)
                m = re_link.search(line_content)
                # check that all references have links
                if not m:
                    if fix_refs:
                        edits[path].append(Edit(line, ref, expected))
                    else:
                        issue_list.append(f"Reference without a link: {ref} in {path}({line + 1})")
                    continue
                actual = m.group(1)
                # check that all links are correct
                if expected != actual:
                    # or update if fix_refs is True
                    if fix_refs:
                        edits[path].append(Edit(line, actual, expected))
                    else:
                        issue_list.append(
                            f"Reference has bad link: {ref} in {path}({line + 1}) is {actual} but should be {expected}",
                        )

    for path, edit_list in edits.items():
        update_file(path, edit_list)

    return issue_list


def closest_string(needle: str, haystack: list[str]) -> str:
    """Find the closest matching string."""
    best_guess = ""
    best_score = 0.0
    for guess in haystack:
        score = SequenceMatcher(a=needle, b=guess).ratio()
        if score > best_score:
            best_score = score
            best_guess = guess
    return best_guess


def gather_markdown_sections_and_refs(
    file_list: list[Path],
    prefix: str,
    ignored_refs: list[str],
) -> tuple[TARGETS_DICT, REFS_DICT]:
    """Gather the sections and all possible references."""
    targets: dict[str, tuple[Path, int]] = {}
    references: defaultdict[str, list[tuple[Path, int]]] = defaultdict(list)
    re_section = get_section_pattern_from_prefix(prefix)
    re_reference = get_section_reference_pattern_from_prefix(prefix)
    ignored = [re.compile(ref) for ref in ignored_refs]

    for path in file_list:
        content = path.read_text()
        for target, line in get_matches_from_md(content, re_section).items():
            if any(ig.match(target) for ig in ignored):
                continue
            targets[target] = (path, line)
        for reference, line in get_matches_from_md(content, re_reference).items():
            # skip any that are actually sections
            if (path, line) in targets.values():
                continue
            if any(ig.match(reference) for ig in ignored):
                continue
            references[reference].append((path, line))

    return targets, references


def update_file(
    file_path: Path,
    edit_list: list[Edit],
) -> None:
    """Update a line in a file using a replace."""
    lines = file_path.read_text().split("\n")
    for edit in edit_list:
        lines[edit.line] = lines[edit.line].replace(edit.actual, edit.replacement)
    file_path.write_text("\n".join(lines))


def get_section_pattern_from_prefix(prefix: str) -> re.Pattern[str]:
    """Return a regular expression for use when capturing valid section headers."""
    return re.compile(rf"^#+ ({prefix}_\w+)$")


def get_section_reference_pattern_from_prefix(prefix: str) -> re.Pattern[str]:
    """Return a regular expression for use when capturing section references."""
    return re.compile(rf"(\b{prefix}_\w+\b)")


def get_link_pattern_from_reference(reference: str) -> re.Pattern[str]:
    """Return a regular expression for use when capturing section references."""
    return re.compile(rf"(\[{reference}\]\([\w\-\./#]+\))")


def get_matches_from_md(md_content: str, section_matcher: re.Pattern[str]) -> dict[str, int]:
    """Get a dictionary of targets to line numbers from a file."""
    targets: dict[str, int] = {}
    for line_number, text in enumerate(md_content.split("\n")):
        for m in section_matcher.finditer(text):
            targets[m.group(1)] = line_number
    return targets
