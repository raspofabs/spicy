"""System requirement spec element."""

import logging
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, render_node

from .spec_element import SpecElement

logger = logging.getLogger(__name__)


class SystemRequirement(SpecElement):
    """Handles system requirements parsing."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="System Requirement")
        self.content: list[str] = []

    def fulfils(self) -> list[str]:
        """Return a list of names of stakeholder requirements this system requirement resolves."""
        return []

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SYS_REQ_1_1_cookie_ordering
        return "_SYS_REQ_" in header_text

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        logger.debug("Parsing as system requirement: %s", node.pretty(show_text=True))
        self.content.append(render_node(node))

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
