"""Stakeholder need spec element."""

import logging
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, parse_yes_no

from .spec_element import SpecElement

logger = logging.getLogger(__name__)


class StakeholderNeed(SpecElement):
    """Handles stakeholder needs parsing."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="Stakeholder Need")
        self.elicitation_date: str | None = None
        self._is_safety_related: bool | None = None

    @property
    def is_safety_related(self) -> bool:
        """Return whether this need has been marked as safety related."""
        if self._is_safety_related is not None:
            return self._is_safety_related
        return False

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_STK_NEED_get_a_cookie
        return "_STK_NEED_" in header_text

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        logger.debug("Parsing as stakeholder need: %s", node.pretty(show_text=True))
        if value := self.single_line_getter(node, "Elicitation date:"):
            self.elicitation_date = value
        if value := self.single_line_getter(node, "Safety related:"):
            self._is_safety_related = parse_yes_no(value)

    def get_issues(self) -> list[str]:
        """Get issues with this spec."""
        if self.elicitation_date is None:
            return ["No elicitation date."]
        return []
