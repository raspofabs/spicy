"""Support reading markdown files into usable syntax trees."""

import logging
from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from mdformat.renderer import MDRenderer

logger = logging.getLogger(__name__)

# create the markdown objects for general use

md = MarkdownIt()
md_renderer = MDRenderer()

# Loading functions


def parse_text_to_syntax_tree(text: str) -> SyntaxTreeNode:
    """Return SyntaxTreeNode for the root of the markdown text."""
    tokens = list(md.parse(text))
    return SyntaxTreeNode(tokens)


def load_syntax_tree(markdown_file_path: Path) -> SyntaxTreeNode:
    """Return SyntaxTreeNode for the root of the markdown file."""
    with markdown_file_path.open() as fh:
        md_file = fh.read()
    return parse_text_to_syntax_tree(md_file)


def parse_yes_no(value: str) -> bool | None:
    """Parse a yes/no answer into a boolean, or return None."""
    value = value.strip().lower()
    if value == "yes":
        return True
    if value == "no":
        return False
    return None


# SyntaxTreeNode interpretation functions


def render_node(node: SyntaxTreeNode) -> str:
    """Return the text of a md node."""
    return md_renderer.render(node.to_tokens(), md.options, {})


def get_text_from_node(node: SyntaxTreeNode) -> str:
    """Return the text of a md node."""
    buffer = ""
    if node.type == "text":
        buffer = node.content
    elif node.type == "code_inline":
        buffer = f"`{node.content}`"
    elif node.type == "code_block":
        buffer = f"`{node.content.strip()}`"

    for child in node.children:
        buffer = (buffer + " " + get_text_from_node(child)).strip()
    return buffer.strip()


def check_node_is(node: SyntaxTreeNode, type_name: str, message: str | None = None) -> None:
    """Check a node is a specific type, raise an IndexError if not."""
    if node.type != type_name:
        msg = (message or f"Node not {type_name}") + f" - was {node.type}"
        raise IndexError(msg)


def list_item_parts(node: SyntaxTreeNode) -> list[SyntaxTreeNode] | None:
    """Return the item parts for a list node."""
    check_node_is(node, "list_item", "node must be a list_item")
    try:
        paragraph_node = node.children[0]
    except IndexError:
        return None
    check_node_is(paragraph_node, "paragraph", "first child node must be a paragraph")
    try:
        inline_node = paragraph_node.children[0]
    except IndexError:  # pragma: no cover
        return None
    check_node_is(inline_node, "inline", "paragraph must start with inline node")
    return inline_node.children


def split_list_item(node: SyntaxTreeNode) -> tuple[str, str]:
    """Split a list_item node into it's leading title and trailing content."""
    parts = list_item_parts(node)
    if parts is None:
        return ("", "")
    try:
        __, title_node, *content_parts = parts
        # collect all the text with content.
        text_parts = filter(lambda x: x.strip(), map(get_text_from_node, content_parts))
        # return as a single string.
        return get_text_from_node(title_node), " ".join(text_parts)
    except ValueError:
        # nothing
        return ("", "")


def read_bullet_list(node: SyntaxTreeNode) -> list[SyntaxTreeNode]:
    """Return the lines of the bullet_list item."""
    if node.type != "bullet_list":
        msg = f"Node is wrong type: {node.type}"
        raise TypeError(msg)
    return [item.children[0] for item in node.children]


def read_titled_bullet_list(node: SyntaxTreeNode) -> dict[str, str]:
    """Return the content of the bullet_list item for the specified variant."""
    if node.type != "bullet_list":
        msg = f"Node is wrong type: {node.type}"
        raise TypeError(msg)
    items = (split_list_item(item) for item in node.children)
    return dict(filter(lambda x: x[0], items))
