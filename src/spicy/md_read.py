"""Support reading markdown files into usable syntax trees."""
from pathlib import Path
from typing import Tuple

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

# Loading function


def parse_text_to_syntax_tree(text: str) -> SyntaxTreeNode:
    """Return SyntaxTreeNode for the root of the markdown text."""
    md = MarkdownIt()
    tokens = list(md.parse(text))
    return SyntaxTreeNode(tokens)


def load_syntax_tree(markdown_file_path: Path) -> SyntaxTreeNode:
    """Return SyntaxTreeNode for the root of the markdown file."""
    with markdown_file_path.open() as fh:
        md_file = fh.read()
    return parse_text_to_syntax_tree(md_file)


# SyntaxTreeNode interpretation functions


def get_text_from_node(node: SyntaxTreeNode) -> str:
    """Return the text of a md node."""
    buffer = ""
    if node.type == "text":
        buffer = node.content
    if node.type == "code_inline":
        buffer = f"`{node.content}`"
    for child in node.children:
        buffer = (buffer + "\n" + get_text_from_node(child)).strip()
    return buffer


def list_item_parts(node: SyntaxTreeNode):
    """Return the item parts for a list node."""
    try:
        assert node.type == "list_item", f"node must be a list_item - was {node.type}"
        paragraph_node = node.children[0]
        assert paragraph_node.type == "paragraph", f"first child node must be a paragraph - was {paragraph_node.type}"
        inline_node = paragraph_node.children[0]
        assert inline_node.type == "inline", f"paragraph must start with inline node - was {inline_node.type}"
        return inline_node.children
    except IndexError:
        # don't have the necessary parts
        return None


def split_list_item(node: SyntaxTreeNode) -> Tuple[str, str]:
    """Split a list_item node into it's leading title and trailing content."""
    parts = list_item_parts(node)
    if parts is None:
        return ("", "")
    __, title_node, *content_parts = parts
    # collect all the text with content.
    text_parts = filter(lambda x: x.strip(), map(get_text_from_node, content_parts))
    # return as a single string.
    return get_text_from_node(title_node), " ".join(text_parts)
