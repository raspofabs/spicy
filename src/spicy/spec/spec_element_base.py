"""Base spec element."""
# pragma: exclude file

import logging
from pathlib import Path

from markdown_it.tree import SyntaxTreeNode

from spicy.md_read import get_text_from_node, parse_yes_no

logger = logging.getLogger(__name__)


class SpecElementBase:
    """Base class for all spec element types."""

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

        self._qualification_related: bool | None = None

    def get_linked(self, _linkage_term: str) -> list[str]:
        """Return a list of all specs linked by this term."""
        return []

    @property
    def is_qualification_related(self) -> bool:
        """Return whether this need has been marked as qualification related."""
        if self._qualification_related is not None:
            return self._qualification_related
        return False

    @staticmethod
    def is_spec_heading(_header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # Always False for base class
        return False

    @staticmethod
    def is_detail_heading(node: SyntaxTreeNode) -> str | None:
        """Return whether this node is a leader for some details."""
        text = get_text_from_node(node).lower()
        if "\n" not in text and text.endswith(":"):
            return text.strip(":").lower()
        if node.type == "heading":
            return get_text_from_node(node).lower().strip(":")
        return None

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode for common features."""
        logger.debug("Parsing common features")
        if value := self.single_line_getter(node, "Safety related:"):
            self._qualification_related = parse_yes_no(value)
        if value := self.single_line_getter(node, "Qualification relevant:"):
            self._qualification_related = parse_yes_no(value)
        if value := self.single_line_getter(node, "TCL relevant:"):
            self._qualification_related = parse_yes_no(value)

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


class IgnoredComponent(SpecElementBase):
    """Handles intentionally ignored components."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="Ignored Component")

    def fulfils(self) -> list[str]:
        """Return nothing."""
        return []

    @staticmethod
    def is_spec_heading(_header_text: str) -> bool:
        """Return false because we are not a parsing node, but a null object of sorts."""
        return False

    def parse_node(self, _node: SyntaxTreeNode) -> None:
        """Don't parse a SyntaxTreeNode."""

    def get_issues(self) -> list[str]:
        """Return no issues."""
        return []
