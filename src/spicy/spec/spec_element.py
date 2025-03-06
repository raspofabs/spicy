"""Base spec element."""

import logging
from pathlib import Path

from spicy.md_read import SyntaxTreeNode

logger = logging.getLogger(__name__)


class SpecElement:
    """Gather information on use-cases and feedback on missing elements."""

    def __init__(
        self,
        name: str,
        ordering_id: int,
        file_path: Path,
        *,
        spec_type: str = "base",
    ) -> None:
        """Construct the basic properties."""
        self.name = name
        self.spec_type = spec_type
        self.ordering_id = ordering_id
        self.file_path = file_path

    @staticmethod
    def is_spec_heading(_header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # Always False for base class
        return False

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        logger.info("Unable to parse, unknown element type: %s", node.pretty(show_text=True))

    def get_issues(self) -> list[str]:
        """Get issues with this spec."""
        return [f"Spec {self.name} is of an unknown type."]
