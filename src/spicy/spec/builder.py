"""Construct SpecElements as they are read."""

import logging
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, List

from spicy.md_read import SyntaxTreeNode, get_text_from_node

from .spec_element import SpecElement
from .spec_stakeholder_need import StakeholderNeed
from .spec_stakeholder_requirement import StakeholderRequirement

logger = logging.getLogger("SpecBuilder")


#### CDU_SYS_REQ_1_1_cookie_ordering
#### CDU_SYS_INT_VER_1_setup_cookie_server
#### CDU_SYS_VER_1_order_a_cookie
#### CDU_SYS_ARCH_1_cookie_storage
#### CDU_SWREQ_1_cookie_ordering
#### CDU_SWARCH_1_cookie_database
#### CDU_SWINT_1_cookie_database_crud
#### CDU_SWQUAL_1_cookie_ordering


class SpecElementBuilder:
    """Gather information on spec elements and create them."""

    SPEC_CLASSES = [
        StakeholderNeed,
        StakeholderRequirement,
    ]

    def __init__(self, name: str, ordering_id: int, file_path: Path):
        """Construct the basic properties."""
        self.name = name
        self.ordering_id = ordering_id
        self.file_path = file_path
        self.content: DefaultDict[str, List[str]] = defaultdict(list)

        self.spec_class = SpecElementBuilder._class_for_header(name)
        self.spec_element = self.spec_class(
            self.name,
            self.ordering_id,
            self.file_path,
        )

    def build(self) -> SpecElement:
        """Build a SpecElement from the gathered data."""
        return self.spec_element

    @property
    def location(self):
        """Return a string for the location of the spec element."""
        return f"{self.file_path}:{self.ordering_id}:{self.name}"

    def _section_add_paragraph(self, section_id: str, content: str):
        """Append content to section information."""
        self.content[section_id].append(content)

    @staticmethod
    def _parse_syntax_tree_to_spec_elements(
        project_prefix: str, tree_root: SyntaxTreeNode, from_file: Path
    ) -> List[SpecElement]:
        """Parse a markdown-it node tree into a list of spec elements."""
        spec_element_builders: List[SpecElementBuilder] = []
        num_specs = 0
        element_prefix = project_prefix.upper() + "_"

        builder = None

        for node in tree_root.children:
            # print(node.pretty())
            if node.type == "heading":
                node_text = get_text_from_node(node)
                print(f"Heading: {node} - {node_text}")
                if element_prefix in node_text:
                    spec_name = element_prefix + node_text.strip().split(element_prefix)[1]
                    num_specs += 1
                    builder = SpecElementBuilder(spec_name, num_specs, from_file)
                    spec_element_builders.append(builder)

            if builder:
                if node.type == "paragraph":
                    text_content = get_text_from_node(node)
                    if builder is not None:
                        builder._section_add_paragraph("content", text_content)
        return [spec.build() for spec in spec_element_builders]

    @staticmethod
    def _class_for_header(name: str):
        for spec_class in SpecElementBuilder.SPEC_CLASSES:
            if spec_class.is_spec_heading(name):
                return spec_class
        else:
            return SpecElement
