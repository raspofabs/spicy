"""Software requirement spec element."""

from typing import Callable, List

from spicy.md_read import render_node

from .spec_element import SpecElement


class SoftwareRequirement(SpecElement):
    """Handles software requirements parsing."""

    def __init__(self, *args):
        """Construct super and placeholder fields."""
        super().__init__(*args, spec_type="Software Requirement")
        self.content = []

    def fulfils(self) -> List[str]:
        """Return a list of names of system elements from which this software requirement is derived."""
        return []

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SW_REQ_cookie_order_persistence
        if "_SW_REQ_" in header_text:
            return True
        return False

    def parse_node(self, node):
        """Parse a SyntaxTreeNode."""
        # logger.info(f"Parsing as software requirement: {node.pretty(show_text=True)}")
        self.content.append(render_node(node))

    def render_issues(self, render_function: Callable) -> bool:
        """Render issues with this spec."""
        return False
