"""Stakeholder requirement spec element."""

from typing import List

from spicy.md_read import render_node

from .spec_element import SpecElement


class SystemRequirement(SpecElement):
    """Handles system requirements parsing."""

    def __init__(self, *args):
        """Construct super and placeholder fields."""
        super().__init__(*args)
        self.content = []

    def fulfils(self) -> List[str]:
        """Return a list of names of system elements this system requirement satisfy fulfils."""
        return []

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SYS_REQ_1_1_cookie_ordering
        if "_SYS_REQ_" in header_text:
            return True
        return False

    def parse_node(self, node):
        """Parse a SyntaxTreeNode for SpecElement."""
        print(f"Parsing as system requirement: {node.pretty(show_text=True)}")
        self.content.append(render_node(node))
