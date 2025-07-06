"""Test the fixes.py module."""

from pathlib import Path

from spicy.fixes import apply_replacements_to_files, build_link_replacements, fix_reference_links


class DummyElement:
    """Stand-in for SpecElement for testing."""

    def __init__(self, file_path: Path, expected_links: dict[str, list[tuple[str, str]]] | None = None) -> None:
        """Initialise the data for testing."""
        self.file_path = file_path
        self.expected_links: dict[str, list[tuple[str, str]]] = expected_links if expected_links is not None else {}


def test_build_link_replacements() -> None:
    """Test build_link_replacements correctly builds a dictionary.

    The dictionary should map file paths to lists of (before, after) link
    replacements from a list of elements.
    The test verifies that elements with None for expected_links are ignored.
    """
    elements: list[DummyElement] = [
        DummyElement(
            file_path=Path("file1.md"),
            expected_links={
                "section1": [("target1", "[target1](#target1)")],
                "section2": [("target2", "[target2](#target2)")],
            },
        ),
        DummyElement(
            file_path=Path("file2.md"),
            expected_links={
                "section3": [("target3", "[target3](#target3)")],
            },
        ),
        DummyElement(file_path=Path("file3.md")),
    ]
    expected: dict[Path, list[tuple[str, str]]] = {
        Path("file1.md"): [
            ("- target1", "- [target1](#target1)"),
            ("- target2", "- [target2](#target2)"),
        ],
        Path("file2.md"): [
            ("- target3", "- [target3](#target3)"),
        ],
    }
    result = build_link_replacements(elements)  # type: ignore[arg-type]
    assert result == expected


def test_apply_replacements_to_files(tmp_path: Path) -> None:
    """Test apply_replacements_to_files correctly applies the provided patches."""
    file1 = Path(tmp_path / "file1.md")
    file2 = Path(tmp_path / "file2.md")
    file1.write_text("- target1\n- target2\n", encoding="utf-8")
    file2.write_text("- target3\n", encoding="utf-8")
    replacements: dict[Path, list[tuple[str, str]]] = {
        file1: [("- target1", "- [target1](#target1)"), ("- target2", "- [target2](#target2)")],
        file2: [("- target3", "- [target3](#target3)")],
    }
    apply_replacements_to_files(replacements)
    assert file1.read_text(encoding="utf-8") == "- [target1](#target1)\n- [target2](#target2)\n"
    assert file2.read_text(encoding="utf-8") == "- [target3](#target3)\n"


def test_fix_reference_links_integration(tmp_path: Path) -> None:
    """Test the integration with fix_reference_links.

    This validates the higher abstraction function builds replacements and
    applies them to the files as expected.
    """
    file1: Path = tmp_path / "file1.md"
    file1.write_text("- target1\n", encoding="utf-8")
    elements: list[DummyElement] = [
        DummyElement(
            file_path=file1,
            expected_links={"section1": [("target1", "[target1](#target1)")]},
        ),
    ]
    fix_reference_links(elements)  # type: ignore[arg-type]
    assert file1.read_text(encoding="utf-8") == "- [target1](#target1)\n"
