"""Stakeholder need spec element."""

from spicy.md_read import render_node

from .spec_element import SpecElement


class StakeholderNeed(SpecElement):
    """Handles stakeholder needs parsing."""

    def __init__(self, *args):
        """Construct super and placeholder fields."""
        super().__init__(*args)
        self.content = []

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_STK_REQ_1_cookie_orders
        if "_STK_NEED_" in header_text:
            return True
        return False

    def parse_node(self, node):
        """Parse a SyntaxTreeNode for SpecElement."""
        print(f"Parsing as stakeholder need: {node.pretty(show_text=True)}")
        self.content.append(render_node(node))
