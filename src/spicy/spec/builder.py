"""Construct SpecElements as they are read."""
# pragma: exclude file

import logging
from collections import defaultdict
from pathlib import Path

from markdown_it.tree import SyntaxTreeNode

from spicy.md_read import get_text_from_node

from .spec_element_base import SpecElementBase
from .spec_software_component import SoftwareComponent
from .spec_software_requirement import SoftwareRequirement
from .spec_software_unit import SoftwareUnit
from .spec_stakeholder_need import StakeholderNeed
from .spec_stakeholder_requirement import StakeholderRequirement
from .spec_system_element import SystemElement
from .spec_system_integration import SystemIntegrationTest
from .spec_system_qualification import SystemQualificationTest
from .spec_system_requirement import SystemRequirement
from .spec_validation import ValidationTest

logger = logging.getLogger("SpecBuilder")


#### CDU_SYS_INT_setup_cookie_server
#### CDU_SYS_QUAL_order_a_cookie
#### CDU_SWINT_1_cookie_database_crud
#### CDU_SWQUAL_1_cookie_ordering


class SpecElementBuilder:
    """Gather information on spec elements and create them."""

    SPEC_CLASSES = (
        StakeholderNeed,
        StakeholderRequirement,
        SystemRequirement,
        SystemElement,
        SoftwareRequirement,
        SoftwareComponent,
        SoftwareUnit,
        SystemIntegrationTest,
        SystemQualificationTest,
        ValidationTest,
    )

    def __init__(self, name: str, ordering_id: int, file_path: Path) -> None:
        """Construct the basic properties."""
        self.name = name
        self.ordering_id = ordering_id
        self.file_path = file_path
        self.content: defaultdict[str, list[str]] = defaultdict(list)

        self.spec_class = SpecElementBuilder._class_for_header(name)
        self.spec_element = self.spec_class(
            self.name,
            self.ordering_id,
            self.file_path,
        )
        self.is_rejected = False

    def build(self) -> SpecElementBase:
        """Build a SpecElementBase from the gathered data."""
        return self.spec_element

    @property
    def location(self) -> str:
        """Return a string for the location of the spec element."""
        return f"{self.file_path}:{self.ordering_id}:{self.name}"

    def section_add_paragraph(self, section_id: str, content: str) -> None:
        """Append content to section information."""
        self.content[section_id].append(content)

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Ask the current spec_element to parse the node."""
        self.spec_element.parse_node(node)

    @staticmethod
    def parse_syntax_tree_to_spec_elements(
        project_prefix: str,
        tree_root: SyntaxTreeNode,
        from_file: Path,
    ) -> list[SpecElementBase]:
        """Parse a markdown-it node tree into a list of spec elements."""
        spec_element_builders: list[SpecElementBuilder] = []
        spec_heading_level = "h1"  # default heading is top level
        num_specs = 0
        element_prefix = project_prefix.upper() + "_"

        builder = None

        for node in tree_root.children:
            logger.debug("%s", node.pretty())
            if node.type == "heading":
                node_text = get_text_from_node(node)
                logger.debug("Heading: %s - %s", node, node_text)
                if element_prefix in node_text:
                    spec_name = node_text.strip()
                    prefix, *postfix = spec_name.split(element_prefix)
                    spec_heading_level = node.tag
                    num_specs += 1
                    builder = SpecElementBuilder(spec_name, num_specs, from_file)
                    if prefix != "REJECTED_":
                        spec_element_builders.append(builder)
                    continue
                if spec_heading_level > node.tag:
                    # higher (lower) level or equal means we're no longer in that spec
                    builder = None
            if builder:
                builder.parse_node(node)
                if node.type == "paragraph":
                    text_content = get_text_from_node(node)
                    if builder is not None:
                        builder.section_add_paragraph("content", text_content)
        return [spec.build() for spec in spec_element_builders]

    @staticmethod
    def _class_for_header(name: str) -> type[SpecElementBase]:
        for spec_class in SpecElementBuilder.SPEC_CLASSES:
            if spec_class.is_spec_heading(name):
                return spec_class
        return SpecElementBase
