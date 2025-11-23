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


def check_markdown_refs(  # noqa: PLR0913, PLR0912 - yeah, this is big.
    file_list: list[Path],
    *,
    base_path: Path,
    prefix: str,
    fix_refs: bool,
    ignored_refs: list[str],
    helpful: bool = False,
) -> list[str]:
    """Check matching refs are correctly linked, optionally fixing them."""
    files = {path: path.read_text().split("\n") for path in file_list}
    targets, references = gather_markdown_sections_and_refs(files, prefix, ignored_refs)

    absolute_links = {
        target: f"[{target}](/{path.relative_to(base_path)}#{target.lower()})" for target, (path, _) in targets.items()
    }
    valid_targets = list(targets)

    issue_list = []

    edits: dict[Path, list[Edit]] = defaultdict(list)

    # check for completely invalid references
    for ref, list_of_locations in references.items():
        re_link = get_link_pattern_from_reference(ref)
        for path, line in list_of_locations:
            if ref not in targets:
                best_alternative = f" Did you mean {closest_string(ref, valid_targets)}" if helpful else ""
                issue = f"Bad reference found: {ref} in {path}({line + 1}) has no matching section."
                issue_list.append(f"{issue}{best_alternative}")
            else:
                # all supported link possibilties
                target_path, _ = targets[ref]
                local_link = f"[{ref}](#{ref.lower()})" if path == targets[ref][0] else None
                absolute_link = absolute_links[ref]
                if path.parent in target_path.parents:
                    relative_link = f"[{ref}]({target_path.relative_to(path.parent)}#{ref.lower()})"
                else:
                    relative_link = absolute_link

                expected = local_link or relative_link

                line_content = files[path][line]
                m = re_link.search(line_content)
                # check that all references have links
                if not m:
                    if fix_refs:
                        edits[path].append(Edit(line, ref, expected))
                    else:
                        issue_list.append(f"Reference without a link: {ref} in {path}({line + 1})")
                    continue
                actual = m.group(1)
                # check that all links are valid
                if actual not in [relative_link, expected, absolute_link]:
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
    file_dict: dict[Path, list[str]],
    prefix: str,
    ignored_refs: list[str],
) -> tuple[TARGETS_DICT, REFS_DICT]:
    """Gather the sections and all possible references."""
    targets: dict[str, tuple[Path, int]] = {}
    references: defaultdict[str, list[tuple[Path, int]]] = defaultdict(list)
    re_section = get_section_pattern_from_prefix(prefix)
    re_reference = get_section_reference_pattern_from_prefix(prefix)
    ignored = [re.compile(ref) for ref in ignored_refs]

    for path, content_lines in file_dict.items():
        for target, lines in get_matches_from_md(content_lines, re_section).items():
            # Ignore any duplicate sections. Take the first one as valid.
            line, *_ = lines
            if any(ig.fullmatch(target) for ig in ignored):
                continue
            targets[target] = (path, line)
        for reference, lines in get_matches_from_md(content_lines, re_reference).items():
            for line in lines:
                # skip any that are actually sections
                if (path, line) in targets.values():
                    continue
                if any(ig.fullmatch(reference) for ig in ignored):
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


def get_matches_from_md(md_content_lines: list[str], section_matcher: re.Pattern[str]) -> dict[str, list[int]]:
    """Get a dictionary of targets to line numbers from a file."""
    targets: dict[str, list[int]] = defaultdict(list)
    for line_number, text in enumerate(md_content_lines):
        for m in section_matcher.finditer(text):
            targets[m.group(1)].append(line_number)
    return targets
