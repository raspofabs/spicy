"""Test the md_link_check.py module."""

import re
import shutil
from pathlib import Path

from spicy.md_link_check import (
    check_markdown_refs,
    get_link_pattern_from_reference,
    get_matches_from_md,
    get_section_pattern_from_prefix,
)


def test_get_section_pattern_from_prefix() -> None:
    """Test the section pattern matches sections based on the prefix."""
    expression = get_section_pattern_from_prefix("ABC")
    assert expression == re.compile(r"^#+ (ABC_\w+)$")
    m = expression.match("# ABC_123")
    assert m
    assert len(m.groups()) > 0
    assert m.group(1) == "ABC_123"

    ref_expression = get_link_pattern_from_reference("ABC_123")
    ref_expression = re.compile(r"(\[ABC_123\]\([\w\./#]+\))")
    assert ref_expression.search("Some text [ABC_123](path.md#anchor) and more.")


def test_get_patterns_match_sections(bad_link_data_path: Path) -> None:
    """Test the section matching pattern matches sections."""
    section_expression = get_section_pattern_from_prefix("BDLNK")

    section_text = "## BDLNK_STK_NEED_have_a_safety_need"
    assert get_matches_from_md(section_text.split("\n"), section_expression)

    content = (bad_link_data_path / "complete_spec.md").read_text()
    all_sections = get_matches_from_md(content.split("\n"), section_expression)
    assert any(section == "BDLNK_STK_NEED_have_a_safety_need" for section in all_sections), all_sections


def test_get_matches_from_md(test_data_path: Path) -> None:
    """Test the get_matches_from_md function can get all valid refs."""
    content = test_data_path / "md_links" / "simple.md"
    found = get_matches_from_md(content.read_text().split("\n"), get_section_pattern_from_prefix("PRE"))
    expected = [
        "PRE_first_heading",
        "PRE_second_heading",
        "PRE_third_heading",
    ]
    assert len(found) == len(expected)
    assert sorted(expected) == sorted(found)
    # check the line numbers are at least in the right order
    assert found["PRE_first_heading"] < found["PRE_second_heading"]


def test_check_markdown_refs(test_data_path: Path, tmpdir: Path) -> None:
    """Test the markdown link checker can find issues."""
    work_dir = Path(tmpdir / "mutable_md")
    shutil.copytree(test_data_path / "md_links", work_dir, dirs_exist_ok=True)

    def check_a_file(file_names: list[str], fix_refs: bool = False, helpful: bool = False) -> list[str]:
        paths = [work_dir / file_name for file_name in file_names]
        return check_markdown_refs(
            paths,
            base_path=work_dir,
            prefix="PRE",
            fix_refs=fix_refs,
            ignored_refs=[],
            helpful=helpful,
        )

    # no links, no issues
    issues = check_a_file(["simple.md"])
    assert not issues

    # correct links, no issues
    issues = check_a_file(["simple.md", "correct.md"])
    assert not issues

    # invalid links, complain about them
    issues = check_a_file(["simple.md", "invalid.md"])
    assert issues
    assert len(issues) == 1
    assert "Reference has bad link" in issues[0]
    assert "Did you mean" not in issues[0]

    # links to unexpected get different complaints
    issues = check_a_file(["simple.md", "inaccurate.md"])
    assert issues
    assert len(issues) == 1
    assert "Bad reference found" in issues[0]
    assert "Did you mean" not in issues[0]

    issues = check_a_file(["simple.md", "inaccurate.md"], helpful=True)
    assert issues
    assert len(issues) == 1
    assert "Bad reference found" in issues[0]
    assert "Did you mean" in issues[0]

    # but not if we fix them
    issues = check_a_file(["simple.md", "invalid.md"], fix_refs=True)
    assert not issues

    # unlinked refs, complain about them
    issues = check_a_file(["simple.md", "unlinked.md"])
    assert issues
    assert "Reference without a link" in issues[0]
    assert len(issues) > 1


def test_check_markdown_refs_in_subdirectories(test_data_path: Path, tmpdir: Path) -> None:
    """Test the markdown link checker can find issues with links in subdirectories."""
    work_dir = Path(tmpdir / "mutable_md")
    shutil.copytree(test_data_path / "md_links", work_dir, dirs_exist_ok=True)

    def check_a_file(file_names: list[str], fix_refs: bool = False, helpful: bool = False) -> list[str]:
        paths = [work_dir / file_name for file_name in file_names]
        return check_markdown_refs(
            paths,
            base_path=work_dir,
            prefix="PRE",
            fix_refs=fix_refs,
            ignored_refs=[],
            helpful=helpful,
        )

    # some issues
    issues = check_a_file(["simple.md", "sub/deeper_refs.md"])
    assert issues
    assert not any("PRE_second_heading" in issue for issue in issues)
    third_issue, *_ = [issue for issue in issues if "PRE_third_heading" in issue]
    # complain about relative, replace with absolute
    assert "(simple" in third_issue
    assert "(/simple" in third_issue

    # some issues
    issues = check_a_file(["simple.md", "sub/deeper.md", "deep_refs.md"])
    expected = ["PRE_deep_second", "PRE_deep_third"]
    for heading in expected:
        assert any(heading in issue for issue in issues)


def test_fixing_markdown_refs_real_data_bad(bad_link_data_path: Path, tmpdir: Path) -> None:
    """Test the markdown link checker can fix real data."""
    work_dir = Path(tmpdir / "mutable_md")
    shutil.copytree(bad_link_data_path, work_dir, dirs_exist_ok=True)

    assert check_markdown_refs(
        [work_dir / "complete_spec.md"],
        base_path=work_dir,
        prefix="BDLNK",
        fix_refs=True,
        ignored_refs=[],
    )

    assert not check_markdown_refs(
        [work_dir / "complete_spec.md"],
        base_path=work_dir,
        prefix="BDLNK",
        fix_refs=True,
        ignored_refs=[
            "BDLNK.*_TEST_.*",
        ],
    )


def test_fixing_markdown_refs_fixes_real_data(fixable_link_data_path: Path, tmpdir: Path) -> None:
    """Test the markdown link checker can fix real data."""
    work_dir = Path(tmpdir / "mutable_md")
    shutil.copytree(fixable_link_data_path, work_dir, dirs_exist_ok=True)
    all_files = list(work_dir.glob("**/*.md"))

    assert not check_markdown_refs(
        all_files,  # [work_dir / "complete_spec.md"],
        base_path=work_dir,
        prefix="FIXME",
        fix_refs=True,
        ignored_refs=[],
    )

    assert not check_markdown_refs(
        all_files,  # [work_dir / "complete_spec.md"],
        base_path=work_dir,
        prefix="FIXME",
        fix_refs=False,
        ignored_refs=[],
    )
