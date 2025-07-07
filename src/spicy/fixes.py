"""Functions to automatically fix issues with a spec."""

from pathlib import Path

from spicy.parser.spec_element import SpecElement


def fix_reference_links(elements: list[SpecElement]) -> None:
    """Build and apply link replacements for a list of elements."""
    replacements = build_link_replacements(elements)
    apply_replacements_to_files(replacements)


def build_link_replacements(elements: list[SpecElement]) -> dict[Path, list[tuple[str, str]]]:
    """Build a dictionary of file -> list of (before, after) link replacements using expected_links."""
    replacements: dict[Path, list[tuple[str, str]]] = {}
    for el in elements:
        for links in el.expected_links.values():
            for _, target_content, md_link in links:
                before = f"- {target_content}"
                after = f"- {md_link}"
                file_path = el.file_path
                replacements.setdefault(file_path, []).append((before, after))
    return replacements


def apply_replacements_to_files(replacements: dict[Path, list[tuple[str, str]]]) -> None:
    """Apply replacements in-place to files as specified by the replacements dict."""
    for file_path, repls in replacements.items():
        if file_path.is_file():
            content = file_path.read_text(encoding="utf-8")
            for before, after in repls:
                content = content.replace(before, after)
            file_path.write_text(content, encoding="utf-8")
