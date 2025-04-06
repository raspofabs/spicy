"""Construct SpecElements as they are read."""

import logging
from collections import defaultdict
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, get_text_from_node, parse_yes_no, split_list_item
from spicy.use_cases.mappings import tcl_map

logger = logging.getLogger("SpecParser")

FEATURES_TITLE = "Features, functions, and technical properties"
DESCRIPTION_OF_USAGE = "Description of usage"
PURPOSE = "Purpose:"
INPUTS = "Inputs:"
OUTPUTS = "Outputs:"
USAGE = "Usage procedure:"
ENVIRONMENT = "Environmental constraints:"
TOOL_IMPACT_HEADING = "Impact analysis of feature"
TOOL_IMPACT_CLASS = "TI class:"
DETECTABILITY_HEADING = "Detectability analysis of feature"
DETECTABILITY_CLASS = "TD class:"

section_map = {
    "": "prologue",
    FEATURES_TITLE: "features",
    DESCRIPTION_OF_USAGE: "usage",
    TOOL_IMPACT_HEADING: "tool_impact",
    DETECTABILITY_HEADING: "detectability",
}

usage_section_map = {
    "inputs": INPUTS,
    "outputs": OUTPUTS,
    "purpose": PURPOSE,
    "usage": USAGE,
    "environment": ENVIRONMENT,
}


class SpecElement:
    """Spec Element class to store details of the spec element and links to other elements."""

    def __init__(
        self,
        name: str,
        variant: str,
        ordering_id: int,
        file_path: Path,
    ) -> None:
        """Construct the basic properties."""
        self.name = name
        self.variant = variant
        self.ordering_id = ordering_id
        self.file_path = file_path

        self._qualification_related: bool | None = None
        self._links: defaultdict[str, list[str]] = defaultdict(list)

        self.title = ""
        self.content: defaultdict[str, list[str]] = defaultdict(list)
        self.impact: str | None = None
        self.detectability: str | None = None
        self.usage_sections: dict[str, str] = {}

    def get_linked_by(self, _linkage_term: str) -> list[str]:
        """Return a list of all specs linked by this term."""
        return self._links.get(_linkage_term, [])

    @property
    def is_qualification_related(self) -> bool:
        """Return whether this need has been marked as qualification related."""
        # All use-cases are qualification relevant if they are TCL2 or TCL3
        if self.variant == "UseCase":
            return self.tcl in ["TCL2", "TCL3"]

        # All requirements and design specs are optionally qualification related
        if self._qualification_related is not None:
            return self._qualification_related
        return False

    def description_text(self) -> list[str]:
        """Return a list of lines describing the use-case."""
        return self.content.get("prologue", [])

    def features_text(self) -> list[str]:
        """Return a list of lines describing the features of the use-case."""
        return self.content.get("features", [])

    def inputs(self) -> str:
        """Return a list of lines describing the inputs of the use-case."""
        return self.usage_sections.get("inputs", "")

    def outputs(self) -> str:
        """Return a list of lines describing the outputs of the use-case."""
        return self.usage_sections.get("outputs", "")

    def impact_rationale(self) -> list[str]:
        """Return a list of lines describing the tool impact of the use-case."""
        return self.content.get("tool_impact", [])

    def detectability_rationale(self) -> list[str]:
        """Return a list of lines describing the error detectability of the use-case."""
        return self.content.get("detectability", [])

    def get_issues(self) -> list[str]:
        """Get issues with this spec."""
        if self.variant == "UseCase":
            return self.get_use_case_issues()
        return self.get_spec_issues()

    def get_spec_issues(self) -> list[str]:
        """Return a list of problems with this spec."""
        return []

    def get_use_case_issues(self) -> list[str]:
        """Return a list of problems with this use case."""
        issues = []
        if self.impact is None:
            issues.append("no impact")
        if self.detectability is None:
            issues.append("no detectability")

        # usage section check
        no_usage = [slot for slot in usage_section_map if slot not in self.usage_sections]
        if no_usage:
            issues.append(f"{len(no_usage)} no usage: {','.join(no_usage)}")

        # section check
        no_section = [slot for slot in section_map.values() if slot not in self.content and slot not in ["usage"]]
        if no_section:
            issues.append(f"{len(no_section)} no section information for :{','.join(no_section)}")

        if issues:
            issues = [f"Issues in {self.file_path.name}, {self.name}", *issues]
        return issues

    @property
    def tcl(self) -> str | None:
        """Return the tcl class based on the tool impact and error detectability."""
        return tcl_map(self.impact, self.detectability)


class SpecElementBuilder:
    """Parses documents and build specs based on found structure."""

    def __init__(self, name: str, variant: str, ordering_id: int, file_path: Path) -> None:
        """Construct the basic properties."""
        self.name = name
        self.ordering_id = ordering_id
        self.file_path = file_path
        self.content: defaultdict[str, list[str]] = defaultdict(list)

        self.spec_element = SpecElement(
            self.name,
            variant,
            self.ordering_id,
            self.file_path,
        )
        self.is_rejected = False
        self.is_qualification_related = False

    def build(self) -> SpecElement:
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
        """Parse a SyntaxTreeNode for common features."""
        logger.debug("Parsing common features")
        if value := self.single_line_getter(node, "Safety related:"):
            self.qualification_related = parse_yes_no(value)
        if value := self.single_line_getter(node, "TCL relevant:"):
            self.qualification_related = parse_yes_no(value)

    def single_line_getter(self, node: SyntaxTreeNode, expected_prefix: str) -> str | None:
        """Get the value from a single line field."""
        text = get_text_from_node(node)
        if text.startswith(expected_prefix):
            __, value = text.split(expected_prefix)
            return value
        return None


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

        self.state = ""

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
        element._links = self.links
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
        self.spec_builders: list[SingleSpecBuilder] = []
        self.header_stack: list[str | None] = [None] * 5
        self.last_heading_level = 0
        self.last_header = ""
        self.last_h2 = ""
        self.last_h3 = ""
        self.num_cases = 0

        self.builder_stack: list[tuple[int, SingleSpecBuilder]] = []
        self.builder: SingleSpecBuilder | None = None
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
        self.header_stack[i - 1] = content
        self.last_header = content
        self.last_heading_level = level
        self.used_current_spec_level = False

        if node.tag == "h2":
            self.used_h2 = False
            self.last_h2 = content
        if node.tag == "h3":
            self.last_h3 = content

        # enable tracking content if the section name matches
        section = section_map.get(self.last_header, self.in_section)
        if section is not None:
            self.in_section = section

        # if self._is_spec_heading(node):
        # self.begin_spec()

    @staticmethod
    def is_spec_heading(_header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # Always False for base class
        return False

    @staticmethod
    def _is_use_case(node: SyntaxTreeNode) -> bool:
        """Return true if the node is a use-case code-block."""
        return node.type == "code_block" and node.content.strip().startswith("ID: ")

    def _handle_use_case_node(self, node: SyntaxTreeNode) -> None:
        use_case_name = node.content.strip().split("ID: ")[1]
        self.in_section = "prologue"
        self.num_cases += 1
        if self.header_stack[-1] is None:
            msg = f"Invalid header stack: {self.header_stack=}"
            raise ValueError(msg)
        self.builder = SingleSpecBuilder(
            use_case_name,
            "UseCase",
            self.num_cases,
            self.from_file,
            self.header_stack[-1],
        )
        self.current_spec_level = self.last_heading_level

        while self.builder_stack and self.builder_stack[-1][0] >= self.current_spec_level:
            self.builder_stack.pop()
        self.builder_stack.append((self.current_spec_level, self.builder))
        if self.used_current_spec_level:
            self.issues.append(f"{self.builder.location} reuses {self.header_stack[-1]} in {self.from_file}")
        self.used_current_spec_level = True
        self.used_h2 = True
        self.spec_builders.append(self.builder)

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
        if self._is_use_case(node):
            self._handle_use_case_node(node)
        elif self.builder is not None:
            if node.type == "paragraph":
                self._handle_paragraph(node)
            elif node.type == "bullet_list":
                self._handle_bullet_list(node)
            elif node.type == "code_block":
                self._handle_code_block(node)


def parse_syntax_tree_to_spec_elements(project_prefix: str, node: SyntaxTreeNode, from_file: Path) -> list[SpecElement]:
    """Parse a markdown-it node tree into a list of Spec Elements."""
    parser = SpecParser(from_file, project_prefix)
    for child in node.children:
        parser.parse_node(child)
    return [spec.build() for spec in parser.spec_builders]


def _parse_syntax_tree_to_spec_elements(
    project_prefix: str,
    tree_root: SyntaxTreeNode,
    from_file: Path,
) -> list[SpecElement]:
    """Parse a markdown-it node tree into a list of Spec Elements."""
    spec_heading_level = "h1"  # default heading is top level
    num_specs = 0
    element_prefix = project_prefix.upper() + "_"

    spec_element_builders: list[SpecElementBuilder] = []
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
                builder = SpecElementBuilder(spec_name, "Spec", num_specs, from_file)
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


# utility functions


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


def _is_detail_heading(node: SyntaxTreeNode) -> str | None:
    """Return whether this node is a leader for some details."""
    text = get_text_from_node(node).lower()
    if "\n" not in text and text.endswith(":"):
        return text.strip(":").lower()
    if node.type == "heading":
        return get_text_from_node(node).lower().strip(":")
    return None
