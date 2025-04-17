"""Software unit spec element."""
# pragma: exclude file

import logging
from pathlib import Path

from markdown_it.tree import SyntaxTreeNode

from spicy.md_read import get_text_from_node, read_bullet_list

from .spec_element_base import SpecElementBase

logger = logging.getLogger(__name__)


class SoftwareUnit(SpecElementBase):
    """Handles software units parsing."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="Software Unit")
        self.content: list[str] = []
        self.implements_list: list[str] = []
        self.state: str = ""

    def fulfils(self) -> list[str]:
        """Return a list of names of software requirements this software unit resolves."""
        return self.implements_list

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SW_UNIT_cookie_ordering_server
        return "_SW_UNIT_" in header_text

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        logger.debug("Parsing as software unit: %s", node.pretty(show_text=True))
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
            issues.append("Missing links for [Implements SoftwareComponent]")
        if issues:
            issues = [f"SoftwareUnit({self.name}):", *issues]
        return issues
