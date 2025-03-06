"""System element spec element."""

from collections.abc import Callable

from spicy.md_read import render_node

from .spec_element import SpecElement


class SystemElement(SpecElement):
    """Handles system architecture parsing."""

    def __init__(self, *args):
        """Construct super and placeholder fields."""
        super().__init__(*args, spec_type="System Element")
        self.content = []

    def fulfils(self) -> list[str]:
        """Return a list of names of system requirements this element fulfils."""
        return []

    def is_software_element(self) -> bool:
        """Return whether this element is a software element."""
        return True

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SYS_ELEMENT_cookie_storage
        if "_SYS_ELEMENT_" in header_text:
            return True
        return False

    def parse_node(self, node):
        """Parse a SyntaxTreeNode."""
        # logger.info(f"Parsing as system architecture: {node.pretty(show_text=True)}")
        self.content.append(render_node(node))

    def render_issues(self, render_function: Callable) -> bool:
        """Render issues with this spec."""
        return False
