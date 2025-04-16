"""Software component spec element."""
# pragma: exclude file

import logging
from pathlib import Path

from markdown_it.tree import SyntaxTreeNode

from spicy.md_read import get_text_from_node, read_bullet_list

from .spec_element_base import SpecElementBase

logger = logging.getLogger(__name__)


class SoftwareComponent(SpecElementBase):
    """Handles software components parsing."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="Software Component")
        self.content: list[str] = []
        self.implements_list: list[str] = []
        self.state: str = ""

    def fulfils(self) -> list[str]:
        """Return a list of names of software requirements this software component resolves."""
        return self.implements_list

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SW_COMP_cookie_database
        return "_SW_COMP_" in header_text

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        logger.debug("Parsing as software component: %s", node.pretty(show_text=True))
        if get_text_from_node(node) == "Implements:":
            self.state = "implements_list"
        if node.type == "bullet_list" and self.state == "implements_list":
            implements_list = read_bullet_list(node)
            self.implements_list.extend([get_text_from_node(x) for x in implements_list])
            self.state = ""

    def get_issues(self) -> list[str]:
        """Get issues with this spec."""
        issues = []
        if not self.implements_list:
            issues.append("Does not implement any software requirement.")
        if issues:
            issues = [f"SoftwareComponent({self.name}):", *issues]
        return issues
