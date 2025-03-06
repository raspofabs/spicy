"""Create a TDP from the documentation."""

import logging
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, List

from spicy.md_read import SyntaxTreeNode, get_text_from_node, split_list_item

from .use_case import UseCase, section_map, usage_section_map

logger = logging.getLogger("UseCases")

TOOL_IMPACT_CLASS = "TI class:"
DETECTABILITY_CLASS = "TD class:"


class UseCaseBuilder:
    """Gather information on use-cases and feedback on missing elements."""

    def __init__(self, name: str, ordering_id: int, file_path: Path, title: str):
        """Construct the basic properties."""
        self.name = name
        self.ordering_id = ordering_id
        self.file_path = file_path
        self.title = title
        self.content: DefaultDict[str, List[str]] = defaultdict(list)
        self.impact = None
        self.detectability = None
        self.usage_sections: Dict[str, str] = {}
        self.needs_fulfilled: List[str] = []

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

    @staticmethod
    def _parse_syntax_tree_to_use_cases(node: SyntaxTreeNode, from_file: Path) -> List[UseCase]:
        """Parse a markdown-it node tree into a list of use cases."""
        use_case_builders: List[UseCaseBuilder] = []
        last_h2 = ""
        last_h3 = ""
        used_h2 = False
        num_cases = 0

        builder = None
        current_use_case = None
        in_section = "none"

        for child in node.children:
            if child.type == "heading":
                if child.tag == "h2":
                    last_h2 = child.children[0].children[0].content
                    used_h2 = False
                if child.tag == "h3":
                    last_h3 = child.children[0].children[0].content
                    in_section = section_map.get(last_h3, in_section)

            if _is_use_case(child):
                use_case_name = child.content.strip().split("ID: ")[1]
                in_section = "prologue"
                num_cases += 1
                builder = UseCaseBuilder(use_case_name, num_cases, from_file, last_h2)
                assert not used_h2, f"{builder.location} reuses {last_h2} in {from_file}"
                used_h2 = True
                use_case_builders.append(builder)
            elif builder:
                if child.type == "paragraph":
                    text_content = get_text_from_node(child)
                    if builder is not None:
                        builder._section_add_paragraph(in_section, text_content)
                elif child.type == "bullet_list":
                    if in_section == "usage":
                        if builder is not None:
                            builder._read_usage_bullets(child)
                elif child.type == "code_block":
                    content = child.content
                    if content.startswith(TOOL_IMPACT_CLASS):
                        assert in_section == "tool_impact", f"Tool impact in {in_section}"
                        impact = content.split(TOOL_IMPACT_CLASS)[1].strip()
                        assert impact in ["", "TI1", "TI2"], f"In {builder.location} == {impact=}"
                        if builder is not None:
                            builder.impact = impact
                    elif content.startswith(DETECTABILITY_CLASS):
                        assert in_section == "detectability", f"Detectabilty in {in_section}"
                        detectability = content.split(DETECTABILITY_CLASS)[1].strip()
                        assert detectability in [
                            "",
                            "TD1",
                            "TD2",
                            "TD3",
                        ], f"In {from_file}:{current_use_case} == {impact=}"
                        if builder is not None:
                            builder.detectability = detectability
                    else:
                        builder._add_code_block(in_section, child)
        return [case.build() for case in use_case_builders]


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


def _list_item_is_variant(parts: List[SyntaxTreeNode], variant: str):
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
