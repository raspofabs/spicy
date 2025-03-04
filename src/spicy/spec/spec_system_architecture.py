"""Stakeholder requirement spec element."""

from spicy.md_read import render_node

from .spec_element import SpecElement


class SystemArchitecture(SpecElement):
    """Handles system architecture parsing."""

    def __init__(self, *args):
        """Construct super and placeholder fields."""
        super().__init__(*args)
        self.content = []

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SYS_ARCH_1_cookie_storage
        if "_SYS_ARCH_" in header_text:
            return True
        return False

    def parse_node(self, node):
        """Parse a SyntaxTreeNode for SpecElement."""
        print(f"Parsing as system architecture: {node.pretty(show_text=True)}")
        self.content.append(render_node(node))
