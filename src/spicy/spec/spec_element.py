"""Base spec element."""

import logging
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, get_text_from_node, parse_yes_no

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

        self._safety_related: bool | None = None

    @property
    def is_safety_related(self) -> bool:
        """Return whether this need has been marked as safety related."""
        if self._safety_related is not None:
            return self._safety_related
        return False

    @staticmethod
    def is_spec_heading(_header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # Always False for base class
        return False

    def parse_node(self, node: SyntaxTreeNode) -> None:
        logger.debug("Parsing common features")
        """Parse a SyntaxTreeNode for common features."""
        if value := self.single_line_getter(node, "Safety related:"):
            self._safety_related = parse_yes_no(value)

    def single_line_getter(self, node: SyntaxTreeNode, expected_prefix: str) -> str | None:
        """Get the value from a single line field."""
        text = get_text_from_node(node)
        if text.startswith(expected_prefix):
            __, value = text.split(expected_prefix)
            return value
        return None

    def get_issues(self) -> list[str]:
        """Get issues with this spec."""
        return [f"Spec {self.name} is of an unknown type."]
