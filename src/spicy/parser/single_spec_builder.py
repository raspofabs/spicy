"""Builder for a single spec. Used by the parser."""

import logging
from collections import defaultdict
from pathlib import Path

from markdown_it.tree import SyntaxTreeNode

from spicy.md_read import read_bullet_list, render_node

from .spec_element import SpecElement
from .use_case_constants import _get_usage_subsection, usage_section_map

logger = logging.getLogger(__name__)


class SingleSpecBuilder:
    """Gather information on specs or use-cases ready to build a SpecElement."""

    def __init__(self, name: str, variant: str, ordering_id: int, file_path: Path, title: str) -> None:
        """Construct the basic properties."""
        self.name = name
        self.ordering_id = ordering_id
        self.file_path = file_path
        self.title = title
        self.content: defaultdict[str, list[str]] = defaultdict(list)
        self.variant = variant
        self.impact: str | None = None
        self.detectability: str | None = None
        self.usage_sections: dict[str, str] = {}
        self.links: defaultdict[str, list[str]] = defaultdict(list)
        self.qualification_related: bool | None = None
        self.software_requirement: bool | None = None
        self.non_functional_requirement: bool | None = None

        self.state = ""
        self.parsing_issues: list[str] = []

    @staticmethod
    def make_null() -> "SingleSpecBuilder":
        """Create a null-object version as a placeholder."""
        return SingleSpecBuilder("null", "null", 0, Path(), "null")

    def build(self) -> SpecElement:
        """Build a Spec Element from the gathered data."""
        element = SpecElement(
            self.name,
            self.variant,
            self.ordering_id,
            self.file_path,
        )

        element.title = self.title
        element.impact = self.impact
        element.content = self.content
        element.impact = self.impact
        element.detectability = self.detectability
        element.usage_sections = self.usage_sections
        if self.qualification_related is not None:
            element.qualification_related = self.qualification_related
        if self.software_requirement is not None:
            element.software_requirement = self.software_requirement
        if self.non_functional_requirement is not None:
            element.non_functional_requirement = self.non_functional_requirement
        return element

    @property
    def location(self) -> str:
        """Return a string for the location of the use case."""
        return f"{self.file_path}:{self.ordering_id}:{self.name}"

    def section_add_paragraph(self, section_id: str, content: str) -> None:
        """Append content to section information."""
        logger.debug("Adding para-content: %s", content)
        self.content[section_id].append(content)

    def add_code_block(self, section_id: str, code_block_node: SyntaxTreeNode) -> None:
        """Use the code block or paste it into content."""
        new_content = code_block_node.content.rstrip()
        logger.debug("Adding code-block: %s", new_content)
        for line in new_content.split("\n"):
            self.content[section_id].append(line)

    def read_bullets_to_section(self, bullet_list: SyntaxTreeNode, section: str) -> None:
        """Consume the bullet list and store in content, preserving markdown links."""
        new_content = list(map(str.rstrip, map(render_node, read_bullet_list(bullet_list))))
        logger.debug("Adding bullets: %s", new_content)
        self.content[section].extend(new_content)

    def read_usage_bullets(self, bullet_list: SyntaxTreeNode) -> None:
        """Consume the usage list and create the usage slot data."""
        for slot, lookup in usage_section_map.items():
            slot_content = _get_usage_subsection(bullet_list, lookup)
            if slot_content:
                self.usage_sections[slot] = slot_content
