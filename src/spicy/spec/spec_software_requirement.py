"""Software requirement spec element."""

import logging
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, get_text_from_node, read_bullet_list

from .spec_element import SpecElement

logger = logging.getLogger(__name__)


class SoftwareRequirement(SpecElement):
    """Handles software requirements parsing."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="Software Requirement")
        self.content: list[str] = []
        self.elements_list: list[str] = []
        self.state = ""

    def fulfils(self) -> list[str]:
        """Return a list of names of system elements from which this software requirement is derived."""
        return self.elements_list

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SW_REQ_cookie_order_persistence
        return "_SW_REQ_" in header_text

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        logger.debug("Parsing as software requirement: %s", node.pretty(show_text=True))
        if get_text_from_node(node) == "Required by:":
            self.state = "elements_list"
        if node.type == "bullet_list" and self.state == "elements_list":
            elements_list = read_bullet_list(node)
            self.elements_list.extend([get_text_from_node(x) for x in elements_list])
            self.state = ""

    def get_issues(self) -> list[str]:
        """Get issues with this spec."""
        issues = []
        if not self.elements_list:
            issues.append("Does not refine from any system element.")
        if issues:
            issues = [f"SoftwareRequirement({self.name}):", *issues]
        return issues
