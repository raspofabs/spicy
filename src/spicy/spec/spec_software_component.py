"""Software component spec element."""

from typing import List

from spicy.md_read import render_node

from .spec_element import SpecElement


class SoftwareComponent(SpecElement):
    """Handles software components parsing."""

    def __init__(self, *args):
        """Construct super and placeholder fields."""
        super().__init__(*args, spec_type="Software Component")
        self.content = []

    def fulfils(self) -> List[str]:
        """Return a list of names of software requirements this software component resolves."""
        return []

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SW_COMP_cookie_database
        if "_SW_COMP_" in header_text:
            return True
        return False

    def parse_node(self, node):
        """Parse a SyntaxTreeNode."""
        print(f"Parsing as software component: {node.pretty(show_text=True)}")
        self.content.append(render_node(node))
