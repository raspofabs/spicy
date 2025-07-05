"""Functions to automatically fix issues with a spec."""

from pathlib import Path


def fix_reference_links(elements: list) -> None:
    """Build and apply link replacements for a list of elements."""
    replacements = build_link_replacements(elements)
    apply_replacements_to_files(replacements)


def build_link_replacements(elements: list) -> dict[str, list[tuple[str, str]]]:
    """Build a dictionary of file -> list of (before, after) link replacements using expected_links."""
    replacements: dict[str, list[tuple[str, str]]] = {}
    for el in elements:
        if el.expected_links is None:
            continue
        for links in el.expected_links.values():
            for target, md_link in links:
                before = f"- {target}"
                after = f"- {md_link}"
                file_path = str(el.file_path)
                replacements.setdefault(file_path, []).append((before, after))
    return replacements


def apply_replacements_to_files(replacements: dict[str, list[tuple[str, str]]]) -> None:
    """Apply replacements in-place to files as specified by the replacements dict."""
    for file_path, repls in replacements.items():
        path = Path(file_path)
        if path.is_file():
            content = path.read_text(encoding="utf-8")
            for before, after in repls:
                content = content.replace(before, after)
            path.write_text(content, encoding="utf-8")
