"""Base spec element."""

import logging
from collections.abc import Callable
from pathlib import Path

logger = logging.getLogger("SpecElement")


class SpecElement:
    """Gather information on use-cases and feedback on missing elements."""

    def __init__(
        self,
        name: str,
        ordering_id: int,
        file_path: Path,
        *,
        spec_type: str = "base",
    ):
        """Construct the basic properties."""
        self.name = name
        self.spec_type = spec_type
        self.ordering_id = ordering_id
        self.file_path = file_path

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # always false for base class
        return False

    def parse_node(self, node):
        """Parse a SyntaxTreeNode."""
        logger.info(f"Unable to parse, unknown element type: {node.pretty(show_text=True)}")

    def render_issues(self, render_function: Callable) -> bool:
        """Render issues with this spec."""
        render_function(f"Spec {self.name} is of an unknown type.")
        return True
