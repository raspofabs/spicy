"""Stakeholder need spec element."""
# pragma: exclude file

import logging
from pathlib import Path

from markdown_it.tree import SyntaxTreeNode

from .spec_element_base import SpecElementBase

logger = logging.getLogger(__name__)


class StakeholderNeed(SpecElementBase):
    """Handles stakeholder needs parsing."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="Stakeholder Need")
        self.elicitation_date: str | None = None

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_STK_NEED_get_a_cookie
        return "_STK_NEED_" in header_text

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        super().parse_node(node)
        logger.debug("Parsing as stakeholder need: %s", node.pretty(show_text=True))
        if value := self.single_line_getter(node, "Elicitation date:"):
            self.elicitation_date = value

    def get_issues(self) -> list[str]:
        """Get issues with this spec."""
        if self.elicitation_date is None:
            return ["No elicitation date."]
        return []
