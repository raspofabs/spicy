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

    def __init__(self, name: str, ordering_id: int, file_path: Path, title: str):
        """Construct the basic properties."""
        self.name = name
        self.ordering_id = ordering_id
        self.file_path = file_path
        self.title = title
        self.content: defaultdict[str, list[str]] = defaultdict(list)
        self.impact = None
        self.detectability = None
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
    def location(self):
        """Return a string for the location of the use case."""
        return f"{self.file_path}:{self.ordering_id}:{self.name}"

    def _section_add_paragraph(self, section_id: str, content: str):
        """Append content to section information."""
        if content.startswith("Fulfils:"):
            self.state = "expect_fulfils"
        else:
            self.content[section_id].append(content)

    def _add_code_block(self, section_id: str, code_block_node: SyntaxTreeNode):
        """Use the code block or paste it into content."""
        if self.state == "expect_fulfils":
            content = code_block_node.content
            self.needs_fulfilled.extend(line.strip() for line in content.split())
            logger.debug(f"{self.name} Adding needs, now: {self.needs_fulfilled}")
            self.state = ""
        else:
            self.content[section_id].append(code_block_node.content)

    def _read_usage_bullets(self, usage_list: SyntaxTreeNode):
        """Consume the usage list and create the usage slot data."""
        for slot, lookup in usage_section_map.items():
            slot_content = _get_usage_subsection(usage_list, lookup)
            if slot_content:
                self.usage_sections[slot] = slot_content


class UseCasesBuilder:
    """Gather information on use-cases and feedback on missing elements."""

    def __init__(self, from_file: Path):
        """Construct the basic properties."""
        self.from_file = from_file
        self.use_case_builders: list[SingleUseCaseBuilder] = []
        self.last_h2 = ""
        self.last_h3 = ""
        self.used_h2 = False
        self.num_cases = 0

        self.builder = None
        self.current_use_case = None
        self.in_section = "none"

    def _handle_heading(self, node):
        if node.tag == "h2":
            self.last_h2 = node.children[0].children[0].content
            self.used_h2 = False
        if node.tag == "h3":
            self.last_h3 = node.children[0].children[0].content
            self.in_section = section_map.get(self.last_h3, self.in_section)

    def _handle_use_case_node(self, node):
        use_case_name = node.content.strip().split("ID: ")[1]
        self.in_section = "prologue"
        self.num_cases += 1
        self.builder = SingleUseCaseBuilder(use_case_name, self.num_cases, self.from_file, self.last_h2)
        assert not self.used_h2, f"{self.builder.location} reuses {self.last_h2} in {self.from_file}"
        self.used_h2 = True
        self.use_case_builders.append(self.builder)

    def _handle_paragraph(self, node):
        text_content = get_text_from_node(node)
        if self.builder is not None:
            self.builder._section_add_paragraph(self.in_section, text_content)

    def _handle_bullet_list(self, node):
        if self.in_section == "usage":
            if self.builder is not None:
                self.builder._read_usage_bullets(node)

    def _handle_code_block(self, node):
        content = node.content
        if content.startswith(TOOL_IMPACT_CLASS):
            assert self.in_section == "tool_impact", f"Tool impact in {self.in_section}"
            impact = content.split(TOOL_IMPACT_CLASS)[1].strip()
            assert impact in ["", "TI1", "TI2"], f"In {self.builder.location} == {impact=}"
            if self.builder is not None:
                self.builder.impact = impact
        elif content.startswith(DETECTABILITY_CLASS):
            assert self.in_section == "detectability", f"Detectabilty in {self.in_section}"
            detectability = content.split(DETECTABILITY_CLASS)[1].strip()
            assert detectability in [
                "",
                "TD1",
                "TD2",
                "TD3",
            ], f"In {self.from_file}:{self.current_use_case} == {impact=}"
            if self.builder is not None:
                self.builder.detectability = detectability
        else:
            self.builder._add_code_block(self.in_section, node)

    def parse_node(self, node):
        """Parse a single node."""
        if node.type == "heading":
            self._handle_heading(node)
        if _is_use_case(node):
            self._handle_use_case_node(node)
        elif self.builder:
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


def _tcl_map(impact: str, detectability: str):
    assert impact in [None, "TI1", "TI2"]
    assert detectability in [None, "TD1", "TD2", "TD3"]
    if impact is None or detectability is None:
        return "<undefined>"
    if impact == "TI1":
        return "TCL1"
    return "TCL" + detectability[-1:]


def _is_use_case(node: SyntaxTreeNode):
    """Return true if the node is a use-case code-block."""
    if node.type == "code_block" and node.content.strip().startswith("ID: "):
        return True


def _list_item_is_variant(parts: list[SyntaxTreeNode], variant: str):
    """Return whether the list item is this variant."""
    try:
        title_node = parts[1]
        if title_node.type != "strong":
            return False
        if title_node.children[0].content == variant:
            return True
    except IndexError:
        logger.warning(f"Malformed bullet_list item {parts}")
        return False
    return False


def _get_usage_subsection(node: SyntaxTreeNode, variant: str):
    """Return the content of the bullet_list item for the specified variant."""
    assert node.type == "bullet_list"
    for bullet_point in node.children:
        title, content = split_list_item(bullet_point)
        if title == variant:
            return content
