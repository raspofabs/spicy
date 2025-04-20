"""Construct SpecElements as they are read."""

import logging
from pathlib import Path

from markdown_it.tree import SyntaxTreeNode

from spicy.md_read import get_text_from_node, parse_yes_no

from .single_spec_builder import SingleSpecBuilder
from .spec_element import SpecElement
from .spec_utils import section_name_to_key, spec_name_to_variant
from .use_case_constants import DETECTABILITY_CLASS, TOOL_IMPACT_CLASS, section_map

logger = logging.getLogger("SpecParser")


class SpecParser:
    """Parses documents and build specs based on found structure."""

    def __init__(self, from_file: Path, project_prefix: str) -> None:
        """Construct the basic properties."""
        self.from_file = from_file
        self.project_prefix = project_prefix

        self.spec_builders: list[SingleSpecBuilder] = []
        self.last_heading_level = 0
        self.last_header = ""
        self.num_cases = 0
        self.parsed_spec_count = 0

        self.builder = SingleSpecBuilder.make_null()
        self.current_spec_level = 0
        self.used_current_spec_level = False
        self.current_use_case = None
        self.in_section: str | None = None
        self.section_is_sticky: bool = False  # headings are sticky, colon-sections are not.

    @property
    def _next_ordering_id(self) -> int:
        self.parsed_spec_count += 1
        return self.parsed_spec_count - 1

    def _handle_heading(self, node: SyntaxTreeNode) -> None:
        # figure out which heading level we're at
        level = int(node.tag[1]) - 1

        content = get_text_from_node(node)
        self.last_header = content
        self.last_heading_level = level
        self.used_current_spec_level = False

        if self.is_spec_heading(content):
            name = content.strip()
            variant = spec_name_to_variant(name) or "Spec"
            title = content
            logger.debug("Found a spec %s", name)
            self.builder = SingleSpecBuilder(name, variant, self._next_ordering_id, self.from_file, title)

            self.current_spec_level = level
            self.used_current_spec_level = True

            prefix, *postfix = name.split(self.project_prefix)
            # don't add to list if it's a rejected spec
            if prefix != "REJECTED_":
                self.spec_builders.append(self.builder)
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
        return bool(node.type == "code_block" and node.content.strip().startswith("ID: "))

    def _handle_use_case_node(self, node: SyntaxTreeNode) -> None:
        use_case_name = node.content.strip().split("ID: ")[1]
        self.in_section = "prologue"
        self.section_is_sticky = True
        self.num_cases += 1
        self.builder = SingleSpecBuilder(
            use_case_name,
            "UseCase",
            self.num_cases,
            self.from_file,
            self.last_header,
        )
        if self.used_current_spec_level:
            self.builder.parsing_issues.append(
                f"{self.builder.location} reuses {self.last_header} in {self.from_file}",
            )

        self.current_spec_level = self.last_heading_level
        self.used_current_spec_level = True

        self.spec_builders.append(self.builder)

    def _handle_paragraph(self, node: SyntaxTreeNode) -> None:
        text_content = get_text_from_node(node)
        if (section_name := looks_like_non_sticky_section(text_content)) is not None:
            section_key = section_name_to_key(section_name)
            logger.debug("looks like non-sticky section %s -> %s", section_name, section_key)
            self.in_section = section_key or section_name
            self.section_is_sticky = False
        elif self.in_section is not None:
            logger.debug("builder add %s -> %s", self.in_section, text_content)
            self.builder.section_add_paragraph(self.in_section, text_content)
            if not self.section_is_sticky:
                self.in_section = None
        else:
            logger.debug("builder didn't add %s (no section)", text_content)

    def _handle_bullet_list(self, node: SyntaxTreeNode) -> None:
        if self.in_section == "usage":
            self.builder.read_usage_bullets(node)
        elif self.in_section is not None:
            self.builder.read_bullets_to_section(node, self.in_section)
        else:  # pragma: no cover
            logger.debug("Unhandled bullet list : %s", node.pretty())

    def _handle_tool_impact(self, content: str) -> None:
        if self.in_section != "tool_impact":
            self.builder.parsing_issues.append(f"Tool impact in {self.in_section}")
        self.impact = content.split(TOOL_IMPACT_CLASS)[1].strip()
        if self.impact not in ["", "TI1", "TI2"]:
            self.builder.parsing_issues.append(f"In {self.builder.location} == {self.impact=}")
        self.builder.impact = self.impact

    def _handle_detectability(self, content: str) -> None:
        if self.in_section != "detectability":
            self.builder.parsing_issues.append(f"Detectabilty in {self.in_section}")
        self.detectability = content.split(DETECTABILITY_CLASS)[1].strip()
        if self.detectability not in ["", "TD1", "TD2", "TD3"]:
            self.builder.parsing_issues.append(f"In {self.builder.location} == {self.detectability=}")
        self.builder.detectability = self.detectability

    def _handle_code_block(self, node: SyntaxTreeNode) -> None:
        content = node.content
        if content.startswith(TOOL_IMPACT_CLASS):
            self._handle_tool_impact(content)
        elif content.startswith(DETECTABILITY_CLASS):
            self._handle_detectability(content)
        elif self.in_section is not None:
            self.builder.add_code_block(self.in_section, node)

    def build_specs(self) -> list[SpecElement]:
        """Build the gathered specs from the builders and return them as a list."""
        return [spec.build() for spec in self.spec_builders]

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a single node."""
        # Parse a SyntaxTreeNode for common features.
        logger.debug("Handle %s: %s", node.type, node.pretty())

        if value := get_if_single_line_section(node):
            section_name, content = value
            section_key = section_name_to_key(section_name)
            logger.debug("Single line section: %s/%s -- %s", section_name, section_key, content)
            if section_key == "qualification_related" and self.builder is not None:
                self.builder.qualification_related = parse_yes_no(content)
                return
            if section_key == "software_requirement" and self.builder is not None:
                self.builder.software_requirement = parse_yes_no(content)
                return

        if self._is_use_case(node):
            logger.debug("Handle use case %s", node.pretty())
            self._handle_use_case_node(node)
            return

        if node.type == "heading":
            logger.debug("Handle heading %s", node.pretty())
            self._handle_heading(node)

        if self.builder is not None:
            logger.debug("Handle %sn%s", node.type, node.pretty())
            if node.type == "paragraph":
                self._handle_paragraph(node)
            elif node.type == "bullet_list":
                self._handle_bullet_list(node)
            elif node.type == "code_block":
                self._handle_code_block(node)
            else:
                logger.debug("Unhandled %s\n%s", node.type, node.pretty())


def parse_syntax_tree_to_spec_elements(project_prefix: str, node: SyntaxTreeNode, from_file: Path) -> list[SpecElement]:
    """Parse a markdown-it node tree into a list of Spec Elements."""
    parser = SpecParser(from_file, project_prefix)
    for child in node.children:
        parser.parse_node(child)
    return parser.build_specs()


# utility functions

MAX_WORDS_IN_SECTION_HEADING = 5


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
    if len(simple_first_line.split(" ")) > MAX_WORDS_IN_SECTION_HEADING:
        return None
    # return the name
    return simple_first_line


def looks_like_single_line_field(text_content: str) -> tuple[str, str] | None:
    """Return the section name if this looks like a single line field, otherwise None."""
    first_line, *lines = text_content.split("\n")
    # single line fields are only a single line.
    if lines:
        return None
    # single line fields always have a single colon and text on both sides
    try:
        simple_preamble, post_colon = first_line.strip().split(":")
        if not simple_preamble:
            return None
        if not post_colon:
            return None
    except ValueError:
        return None
    # are always short on word count
    if len(simple_preamble.split(" ")) > MAX_WORDS_IN_SECTION_HEADING:
        return None
    # return the name
    return simple_preamble, post_colon


def get_if_single_line_section(node: SyntaxTreeNode) -> tuple[str, str] | None:
    """Get the name and value from a single line field, None otherwise."""
    text = get_text_from_node(node)
    return looks_like_single_line_field(text)
