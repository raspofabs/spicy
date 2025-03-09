"""System element spec element."""

import logging
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, get_text_from_node, read_bullet_list

from .spec_element import SpecElement

logger = logging.getLogger(__name__)


class SystemElement(SpecElement):
    """Handles system architecture parsing."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="System Element")
        self.content: list[str] = []
        self.implements_list: list[str] = []
        self.state = ""

    def fulfils(self) -> list[str]:
        """Return a list of names of system requirements this element fulfils."""
        return self.implements_list

    def is_software_element(self) -> bool:
        """Return whether this element is a software element."""
        return True

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SYS_ELEMENT_cookie_storage
        return "_SYS_ELEMENT_" in header_text

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        logger.debug("Parsing as system element: %s", node.pretty(show_text=True))
        if get_text_from_node(node) == "Implements:":
            self.state = "reqs_list"
        if node.type == "bullet_list" and self.state == "reqs_list":
            implemented_reqs = read_bullet_list(node)
            self.implements_list.extend([get_text_from_node(x) for x in implemented_reqs])
            self.state = ""

    def get_issues(self) -> list[str]:
        """Get issues with this spec."""
        return []


# Look for a table of required descriptions
# - **Location:**
# - **Versioning:**
# - **Inputs:**
# - **Outputs:**
# - **Interfaces:**
# - **Sequential coupling:**
# - **Phases:**
