"""Stakeholder requirement spec element."""

from typing import List

from spicy.md_read import render_node

from .spec_element import SpecElement


class StakeholderRequirement(SpecElement):
    """Handles stakeholder requirements parsing."""

    def __init__(self, *args):
        """Construct super and placeholder fields."""
        super().__init__(*args, spec_type="Stakeholder Requirement")
        self.content = []

    def fulfils(self) -> List[str]:
        """Return a list of names of stakeholder needs this requirement fulfils."""
        return []

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_STK_REQ_1_cookie_orders
        if "_STK_REQ_" in header_text:
            return True
        return False

    def parse_node(self, node):
        """Parse a SyntaxTreeNode."""
        print(f"Parsing as stakeholder requirement: {node.pretty(show_text=True)}")
        self.content.append(render_node(node))
