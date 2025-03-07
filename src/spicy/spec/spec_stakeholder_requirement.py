"""Stakeholder requirement spec element."""

import logging
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, get_text_from_node, read_bullet_list

from .spec_element import SpecElement

logger = logging.getLogger(__name__)


class StakeholderRequirement(SpecElement):
    """Handles stakeholder requirements parsing."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="Stakeholder Requirement")
        self.content: list[str] = []
        self.state: str = ""
        self.implements_list: list[str] = []

    def fulfils(self) -> list[str]:
        """Return a list of names of stakeholder needs this requirement fulfils."""
        return self.implements_list

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_STK_REQ_1_cookie_orders
        return "_STK_REQ_" in header_text

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        logger.info("Parsing as stakeholder requirement: %s", node.pretty(show_text=True))
        if get_text_from_node(node) == "Implements:":
            self.state = "needs_list"
        if node.type == "bullet_list" and self.state == "needs_list":
            need_items = read_bullet_list(node)
            self.implements_list.extend([get_text_from_node(x) for x in need_items])
            self.state = ""

    def get_issues(self) -> list[str]:
        """Get issues with this spec."""
        return []


# Implements:
#
# - [CDU_STK_NEED_get_a_cookie](#cdu_stk_need_get_a_cookie)
