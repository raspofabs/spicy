"""System integration test spec element."""

import logging
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, get_text_from_node, read_bullet_list

from .spec_element import SpecElement

logger = logging.getLogger(__name__)


class SystemIntegrationTest(SpecElement):
    """Handles system IntegrationTests parsing."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="System integration test")
        self.content: list[str] = []
        self.integrates_list: list[str] = []
        self.cases_list: list[str] = []
        self.state = ""

    def integrates(self) -> list[str]:
        """Return a list of names of system requirements this system integration test resolves."""
        return self.integrates_list

    def monitors(self) -> list[str]:
        """Return a list of names of test cases this system integration test depends on."""
        return self.cases_list

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SYS_INT_bakery_trigger
        return "_SYS_INT_" in header_text

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        logger.debug("Parsing as system integration test: %s", node.pretty(show_text=True))
        if get_text_from_node(node) == "Integrates:":
            self.state = "component_list"
        if node.type == "bullet_list" and self.state == "component_list":
            tested_reqs = read_bullet_list(node)
            self.integrates_list.extend([get_text_from_node(x) for x in tested_reqs])
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
