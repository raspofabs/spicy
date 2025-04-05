"""System requirement spec element."""

import logging
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, get_text_from_node, read_bullet_list, read_titled_bullet_list

from .spec_element import SpecElement

logger = logging.getLogger(__name__)


class SystemRequirement(SpecElement):
    """Handles system requirements parsing."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="System Requirement")
        self.content: list[str] = []
        self.derived_from_list: list[str] = []
        self.verification_list: list[str] = []
        self.specification: dict[str, str] = {}
        self.state = ""

    def fulfils(self) -> list[str]:
        """Return a list of names of stakeholder requirements this system requirement resolves."""
        return self.derived_from_list

    @property
    def is_qualification_related(self) -> bool:
        """Return whether the spec is safety related based on specification first."""
        if self.specification.get("safety related", "").lower().strip(".") == "yes":
            return True
        if self.specification.get("tcl relevant", "").lower().strip(".") == "yes":
            return True
        return super().is_qualification_related

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SYS_REQ_1_1_cookie_ordering
        return "_SYS_REQ_" in header_text

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        super().parse_node(node)
        detail_heading = self.is_detail_heading(node)

        logger.debug("Parsing as system requirement: %s", node.pretty(show_text=True))
        if detail_heading == "derived from":
            self.state = "reqs_list"
        elif detail_heading == "verification criteria":
            self.state = "verification_list"
        elif detail_heading == "specification":
            self.state = "specification_list"

        if node.type == "code_block" and self.state == "reqs_list":
            reqs_list = [x.strip() for x in node.content.split("\n") if x.strip()]
            self.derived_from_list.extend(reqs_list)
            self.state = ""
        if node.type == "bullet_list":
            if self.state == "reqs_list":
                reqs_list = read_bullet_list(node)
                self.derived_from_list.extend([get_text_from_node(x) for x in reqs_list])
                self.state = ""
            if self.state == "verification_list":
                elements_list = read_bullet_list(node)
                self.verification_list.extend([get_text_from_node(x) for x in elements_list])
                self.state = ""
            if self.state == "specification_list":
                new_spec = {a.strip().strip(":").lower(): b.strip() for a, b in read_titled_bullet_list(node).items()}
                self.specification.update(new_spec)
                self.state = ""

    def get_issues(self) -> list[str]:
        """Get issues with this spec."""
        issues = []
        if not self.verification_list:
            issues.append("Has no verification criteria.")
        if not self.derived_from_list:
            issues.append("Does not derive from any stakeholder requirements.")
        if not self.specification:
            issues.append("Has no detailed specification.")
        if issues:
            issues = [f"SystemRequirement({self.name}):", *issues]
        return issues
