"""Construct SpecElements as they are read."""

import logging
from collections import defaultdict
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, get_text_from_node, parse_yes_no, split_list_item
from spicy.use_cases.mappings import tcl_map
from .spec_element import SpecElement
from .use_case_constants import section_map, usage_section_map, TOOL_IMPACT_CLASS, DETECTABILITY_CLASS
from .spec_utils import spec_name_to_variant

logger = logging.getLogger("SpecParser")

class SingleSpecBuilder:
    """Gather information on use-cases and feedback on missing elements."""

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
        self.qualification_related: bool = False

        self.state = ""

    def build(self) -> SpecElement:
        """Build a Spec Element from the gathered data."""
        element = SpecElement(
            self.name,
            self.variant,
            self.ordering_id,
            self.file_path,
            #links=self.links,
        )

        element.title = self.title
        element.impact = self.impact
        element.content = self.content
        element.impact = self.impact
        element.detectability = self.detectability
        element.usage_sections = self.usage_sections
        if self.qualification_related is not None:
            element._qualification_related = self.qualification_related
        return element

    @property
    def location(self) -> str:
        """Return a string for the location of the use case."""
        return f"{self.file_path}:{self.ordering_id}:{self.name}"

    def section_add_paragraph(self, section_id: str, content: str) -> None:
        """Append content to section information."""
        if content.startswith("Fulfils:"):
            self.state = "expect_fulfils"
        else:
            self.content[section_id].append(content)

    def add_code_block(self, section_id: str, code_block_node: SyntaxTreeNode) -> None:
        """Use the code block or paste it into content."""
        if self.state == "expect_fulfils":
            content = code_block_node.content
            self.links["fulfils"].extend(line.strip() for line in content.split())
            self.state = ""
        else:
            self.content[section_id].append(code_block_node.content)

    def read_usage_bullets(self, usage_list: SyntaxTreeNode) -> None:
        """Consume the usage list and create the usage slot data."""
        for slot, lookup in usage_section_map.items():
            slot_content = _get_usage_subsection(usage_list, lookup)
            if slot_content:
                self.usage_sections[slot] = slot_content


class SpecParser:
    """Parses documents and build specs based on found structure."""

    def __init__(self, from_file: Path, project_prefix: str) -> None:
        """Construct the basic properties."""
        self.from_file = from_file
        self.project_prefix = project_prefix

        self.spec_builders: list[SingleSpecBuilder] = []
        self.header_stack: list[str | None] = [None] * 5
        self.last_heading_level = 0
        self.last_header = ""
        self.num_cases = 0
        self.parsed_spec_count = 0

        self.builder_stack: dict[tuple[int, SingleSpecBuilder]] = {}
        self.builder: SingleSpecBuilder | None = None
        self.current_spec_level = 0
        self.used_current_spec_level = False
        self.current_use_case = None
        self.in_section = "none"
        self.section_is_sticky: bool = False # headings are sticky, colon-sections are not.
        self.issues: list[str] = []

    @property
    def next_ordering_id(self) -> int:
        self.parsed_spec_count += 1
        return self.parsed_spec_count - 1

    def _close_section(self, level: int):
        if self.header_stack[level] is not None:
            if builder := self.builder_stack.get(level) is not None:
                del self.builder_stack[level]
        self.header_stack[level] = None

    def single_line_getter(self, node: SyntaxTreeNode, expected_prefix: str) -> str | None:
        """Get the value from a single line field."""
        text = get_text_from_node(node)
        if text.startswith(expected_prefix):
            __, value = text.split(expected_prefix)
            return value
        return None

    def _handle_heading(self, node: SyntaxTreeNode) -> None:
        # figure out which heading level we're at
        level = int(node.tag[1]) - 1
        # clear all levels below this level (use max key from header_stack)
        for i in reversed(range(level, 5)):
            self._close_section(i)
            self.header_stack[i] = None
        content = get_text_from_node(node)#node.children[0].children[0].content
        self.header_stack[level] = content
        self.last_header = content
        self.last_heading_level = level
        self.used_current_spec_level = False

        if self.is_spec_heading(content):
            self.used_current_spec_level = True
            self.current_spec_level = level
            name = content.strip()
            variant = spec_name_to_variant(name) or "Spec"
            title = content
            logger.debug("Found a spec %s", name)
            builder = SingleSpecBuilder(
                    name,
                    variant,
                    self.next_ordering_id,
                    self.from_file,
                    title)
            self.builder = builder
            self.builder_stack[level] = builder
            prefix, *postfix = name.split(self.project_prefix)
            # don't add to list if it's a rejected spec
            if prefix != "REJECTED_":
                self.spec_builders.append(builder)
            self.in_section = "prologue"
            self.section_is_sticky = True
        else:
            # enable tracking content if the section name matches
            section = section_map.get(self.last_header, self.in_section)
            if section is not None:
                self.in_section = section
                self.section_is_sticky = True

    def is_spec_heading(self, header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        return header_text.startswith(self.project_prefix)

    @staticmethod
    def _is_use_case(node: SyntaxTreeNode) -> bool:
        """Return true if the node is a use-case code-block."""
        return node.type == "code_block" and node.content.strip().startswith("ID: ")

    def _handle_use_case_node(self, node: SyntaxTreeNode) -> None:
        use_case_name = node.content.strip().split("ID: ")[1]
        self.in_section = "prologue"
        self.section_is_sticky = True
        self.num_cases += 1
        if self.header_stack[self.last_heading_level] is None:
            msg = f"Invalid header stack: {self.header_stack=}"
            raise ValueError(msg)
        self.builder = SingleSpecBuilder(
            use_case_name,
            "UseCase",
            self.num_cases,
            self.from_file,
            self.last_header,
        )
        self.current_spec_level = self.last_heading_level
        self.used_current_spec_level = True

        builders_to_delete = [k for k in self.builder_stack if k >= self.current_spec_level]
        for level in builders_to_delete:
            del self.builder_stack[level]
        self.builder_stack[self.current_spec_level] = self.builder

        if self.used_current_spec_level:
            self.issues.append(f"{self.builder.location} reuses {self.header_stack[-1]} in {self.from_file}")
        self.used_current_spec_level = True

        self.spec_builders.append(self.builder)

    def _handle_paragraph(self, node: SyntaxTreeNode) -> None:
        text_content = get_text_from_node(node)
        if (section_name := looks_like_non_sticky_section(text_content)) is not None:
            logger.debug("looks like non-sticky section %s", section_name)
            self.in_section = section_name
            self.section_is_sticky = False
        if self.builder is not None:
            logger.debug("builder add %s -> %s", self.in_section, text_content)
            self.builder.section_add_paragraph(self.in_section, text_content)
            if not self.section_is_sticky:
                self.in_section = None

    def _handle_bullet_list(self, node: SyntaxTreeNode) -> None:
        if self.builder is None:
            return
        if self.in_section == "usage" and self.builder is not None:
            self.builder.read_usage_bullets(node)

    def _handle_code_block(self, node: SyntaxTreeNode) -> None:
        if self.builder is None:
            return
        content = node.content
        if content.startswith(TOOL_IMPACT_CLASS):
            if self.in_section != "tool_impact":
                self.issues.append(f"Tool impact in {self.in_section}")
            self.impact = content.split(TOOL_IMPACT_CLASS)[1].strip()
            if self.impact not in ["", "TI1", "TI2"]:
                self.issues.append(f"In {self.builder.location} == {self.impact=}")
            if self.builder is not None:
                self.builder.impact = self.impact
        elif content.startswith(DETECTABILITY_CLASS):
            if self.in_section != "detectability":
                self.issues.append(f"Detectabilty in {self.in_section}")
            self.detectability = content.split(DETECTABILITY_CLASS)[1].strip()
            if self.detectability not in ["", "TD1", "TD2", "TD3"]:
                self.issues.append(f"In {self.builder.location} == {self.detectability=}")
            if self.builder is not None:
                self.builder.detectability = self.detectability
        else:
            self.builder.add_code_block(self.in_section, node)

    def build_specs(self) -> list[SpecElement]:
        return [spec.build() for spec in self.spec_builders]

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a single node."""
        # Parse a SyntaxTreeNode for common features.
        logger.debug("Handle %s: %s", node.type, node.pretty())

        if value := self.single_line_getter(node, "Safety related:"):
            logger.debug("Parsed safety related")
            self.builder.qualification_related = parse_yes_no(value)
            return
        if value := self.single_line_getter(node, "TCL relevant:"):
            logger.debug("Parsed TCL related")
            self.builder.qualification_related = parse_yes_no(value)
            return
        if value := self.single_line_getter(node, "TQP relevant:"):
            logger.debug("Parsed TQP related")
            self.builder.qualification_related = parse_yes_no(value)
            return

        if self._is_use_case(node):
            logger.debug("Handle use case %s", node.pretty())
            self._handle_use_case_node(node)
            return

        if node.type == "heading":
            logger.debug("Handle heading %s", node.pretty())
            self._handle_heading(node)

        if self.builder is not None:
            if node.type == "paragraph":
                logger.debug("Handle paragraph %s", node.pretty())
                self._handle_paragraph(node)
            elif node.type == "bullet_list":
                logger.debug("Handle bullet-list %s", node.pretty())
                self._handle_bullet_list(node)
            elif node.type == "code_block":
                logger.debug("Handle code-block %s", node.pretty())
                self._handle_code_block(node)


def parse_syntax_tree_to_spec_elements(project_prefix: str, node: SyntaxTreeNode, from_file: Path) -> list[SpecElement]:
    """Parse a markdown-it node tree into a list of Spec Elements."""
    parser = SpecParser(from_file, project_prefix)
    for child in node.children:
        parser.parse_node(child)
    return parser.build_specs()


# utility functions

def looks_like_non_sticky_section(text_content: str) -> str | None:
    """Return the section name if this looks like a section heading, otherwise None."""
    first_line, *lines = text_content.split("\n")
    # headers are only one line
    if lines:
        return None
    # section headers always have a single terminal colon
    try:
        simple_first_line, post_colon = first_line.strip().split(":")
        if post_colon:
            return None
    except ValueError:
        return None
    # are always short on word count
    if len(simple_first_line.split(" ")) > 5:
        return None
    # return the name
    return simple_first_line




def _get_usage_subsection(node: SyntaxTreeNode, variant: str) -> str:
    """Return the content of the bullet_list item for the specified variant."""
    if node.type != "bullet_list":
        msg = f"Node is wrong type: {node.type}"
        raise TypeError(msg)
    for bullet_point in node.children:
        title, content = split_list_item(bullet_point)
        if title == variant:
            return content
    return ""
