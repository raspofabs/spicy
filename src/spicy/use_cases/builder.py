"""Create a TDP from the documentation."""

import logging
from collections import defaultdict
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, get_text_from_node, split_list_item

from .use_case import UseCase, section_map, usage_section_map

logger = logging.getLogger("UseCases")

TOOL_IMPACT_CLASS = "TI class:"
DETECTABILITY_CLASS = "TD class:"


class SingleUseCaseBuilder:
    """Gather information on use-cases and feedback on missing elements."""

    def __init__(self, name: str, ordering_id: int, file_path: Path, title: str) -> None:
        """Construct the basic properties."""
        self.name = name
        self.ordering_id = ordering_id
        self.file_path = file_path
        self.title = title
        self.content: defaultdict[str, list[str]] = defaultdict(list)
        self.impact: str | None = None
        self.detectability: str | None = None
        self.usage_sections: dict[str, str] = {}
        self.needs_fulfilled: list[str] = []

        self.state = ""

    def build(self) -> UseCase:
        """Build a UseCase from the gathered data."""
        return UseCase(
            self.name,
            self.ordering_id,
            self.file_path,
            self.title,
            self.content,
            self.impact,
            self.detectability,
            self.usage_sections,
            self.needs_fulfilled,
        )

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
            self.needs_fulfilled.extend(line.strip() for line in content.split())
            logger.debug("%s Adding needs %s", self.name, self.needs_fulfilled)
            self.state = ""
        else:
            self.content[section_id].append(code_block_node.content)

    def read_usage_bullets(self, usage_list: SyntaxTreeNode) -> None:
        """Consume the usage list and create the usage slot data."""
        for slot, lookup in usage_section_map.items():
            slot_content = _get_usage_subsection(usage_list, lookup)
            if slot_content:
                self.usage_sections[slot] = slot_content


class UseCasesBuilder:
    """Gather information on use-cases and feedback on missing elements."""

    def __init__(self, from_file: Path) -> None:
        """Construct the basic properties."""
        self.from_file = from_file
        self.use_case_builders: list[SingleUseCaseBuilder] = []
        self.header_stack: list[str | None] = [None] * 5
        self.last_heading_level = 0
        self.last_header = ""
        self.last_h2 = ""
        self.last_h3 = ""
        self.num_cases = 0

        self.builder_stack: list[tuple(int, SingleUseCaseBuilder)] = []
        self.builder: SingleUseCaseBuilder | None = None
        self.current_spec_level = 0
        self.used_current_spec_level = False
        self.current_use_case = None
        self.in_section = "none"
        self.issues: list[str] = []

    def _handle_heading(self, node: SyntaxTreeNode) -> None:
        level = int(node.tag[1])
        for i in range(level):
            self.header_stack[i] = None
        content = node.children[0].children[0].content
        self.header_stack[i-1] = content
        self.last_header = content
        self.last_heading_level = level
        self.used_current_spec_level = False

        if node.tag == "h2":
            self.used_h2 = False
            self.last_h2 = content
        if node.tag == "h3":
            self.last_h3 = content
            #self.in_section = section_map.get(self.last_h3, self.in_section)

        # enable tracking content if the section name matches
        section = section_map.get(self.last_header, self.in_section)
        if section is not None:
            self.in_section = section

    def _handle_use_case_node(self, node: SyntaxTreeNode) -> None:
        use_case_name = node.content.strip().split("ID: ")[1]
        self.in_section = "prologue"
        self.num_cases += 1
        self.builder = SingleUseCaseBuilder(use_case_name, self.num_cases, self.from_file, self.header_stack[-1])
        self.current_spec_level = self.last_heading_level

        while self.builder_stack and self.builder_stack[-1][0] >= self.current_spec_level:
            self.builder_stack.pop()
        self.builder_stack.append((self.current_spec_level, self.builder))
        if self.used_current_spec_level:
            self.issues.append(f"{self.builder.location} reuses {self.header_stack[-1]} in {self.from_file}")
        self.used_current_spec_level = True
        self.used_h2 = True
        self.use_case_builders.append(self.builder)

    def _handle_paragraph(self, node: SyntaxTreeNode) -> None:
        text_content = get_text_from_node(node)
        if self.builder is not None:
            self.builder.section_add_paragraph(self.in_section, text_content)

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

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a single node."""
        if node.type == "heading":
            self._handle_heading(node)
        if _is_use_case(node):
            self._handle_use_case_node(node)
        elif self.builder is not None:
            if node.type == "paragraph":
                self._handle_paragraph(node)
            elif node.type == "bullet_list":
                self._handle_bullet_list(node)
            elif node.type == "code_block":
                self._handle_code_block(node)


def parse_syntax_tree_to_use_cases(node: SyntaxTreeNode, from_file: Path) -> list[UseCase]:
    """Parse a markdown-it node tree into a list of use cases."""
    builder = UseCasesBuilder(from_file)
    for child in node.children:
        builder.parse_node(child)
    return [case.build() for case in builder.use_case_builders]


# private functions


def _is_use_case(node: SyntaxTreeNode) -> bool:
    """Return true if the node is a use-case code-block."""
    return node.type == "code_block" and node.content.strip().startswith("ID: ")


def _list_item_is_variant(parts: list[SyntaxTreeNode], variant: str) -> bool:
    """Return whether the list item is this variant."""
    try:
        title_node = parts[1]
        if title_node.type != "strong":
            return False
        if title_node.children[0].content == variant:
            return True
    except IndexError:
        logger.warning("Malformed bullet_list item: %s", parts)
        return False
    return False


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
