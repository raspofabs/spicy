"""System qualification test spec element."""

import logging
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, get_text_from_node, read_bullet_list

from .spec_element import SpecElement

logger = logging.getLogger(__name__)


class SystemQualificationTest(SpecElement):
    """Handles system QualificationTests parsing."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="System qualification test")
        self.content: list[str] = []
        self.tests_list: list[str] = []
        self.cases_list: list[str] = []
        self.state = ""

    def fulfils(self) -> list[str]:
        """Return a list of names of system requirements this system qualification test resolves."""
        return self.tests_list

    def monitors(self) -> list[str]:
        """Return a list of names of test cases this system qualification test depends on."""
        return self.cases_list

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SYS_REQ_1_1_cookie_ordering
        return "_SYS_QUAL_" in header_text

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        logger.debug("Parsing as system qualification test: %s", node.pretty(show_text=True))
        if get_text_from_node(node) == "Tests:":
            self.state = "reqs_list"
        if node.type == "bullet_list" and self.state == "reqs_list":
            tested_reqs = read_bullet_list(node)
            self.tests_list.extend([get_text_from_node(x) for x in tested_reqs])
            self.state = ""
        if get_text_from_node(node) == "Cases:":
            self.state = "cases_list"
        if node.type == "bullet_list" and self.state == "cases_list":
            test_cases = read_bullet_list(node)
            self.cases_list.extend([get_text_from_node(x) for x in test_cases])
            self.state = ""

    def get_issues(self) -> list[str]:
        """Get issues with this spec."""
        return []
