"""Base spec element."""

import logging
from pathlib import Path
from typing import Callable, Optional

logger = logging.getLogger("SpecElement")


class SpecElement:
    """Gather information on use-cases and feedback on missing elements."""

    def __init__(
        self,
        name: str,
        ordering_id: int,
        file_path: Path,
    ):
        """Construct the basic properties."""
        self.name = name
        self.spec_type = "base"
        self.ordering_id = ordering_id
        self.file_path = file_path

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # always false for base class
        return False

    def render_issues(self, render_function: Optional[Callable] = None) -> bool:
        """Render issues with this spec."""
        return False
