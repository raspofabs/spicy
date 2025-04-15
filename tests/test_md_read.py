"""Test the md-doc reading."""

import pytest
from pathlib import Path

from spicy.md_read import (
    list_item_parts,
    load_syntax_tree,
    parse_text_to_syntax_tree,
    render_node,
    parse_yes_no,
    get_text_from_node,
    check_node_is,
    list_item_parts,
    split_list_item,
    read_bullet_list,
    read_titled_bullet_list,
    )


def test_load_markdown_to_syntax_tree(test_data_path: Path) -> None:
    """Test a simple md file load and parse."""
    node = load_syntax_tree(test_data_path / "use_cases" / "01_simple_valid.md")
    assert node is not None


def test_list_item_parts() -> None:
    """Test parsing of list items."""
    root_node = parse_text_to_syntax_tree("- **title:** text content `inline code` more text.")
    assert root_node.type == "root"
    bullet_list = root_node.children[0]
    assert bullet_list.type == "bullet_list"
    bullet_line = bullet_list.children[0]
    assert bullet_line.type == "list_item"

    item_parts = list_item_parts(bullet_line)
    assert item_parts
    # check title
    assert item_parts[1].children[0].content == "title:"
    # check content
    assert item_parts[2].content.strip() == "text content"
    assert item_parts[3].content.strip() == "inline code"
    assert item_parts[4].content.strip() == "more text."

    bullet_line.children = []
    assert list_item_parts(bullet_line) is None


def test_read_and_re_render() -> None:
    """Test the ability to write out what we read."""

    def to_text(lines: list[str]) -> str:
        return "\n".join([*lines, ""])

    sub_content = ["I like to have", "Some quoted text.", "-- me."]
    quoted_content = ["> " + line for line in sub_content]
    test_content = ["#Title", "", "This is some content.", "", *quoted_content, "", "Last content."]
    test_text = to_text(test_content)
    root_node = parse_text_to_syntax_tree(test_text)
    rendered = render_node(root_node)
    assert rendered == test_text

    # make sure there is a block-quote
    assert any(x.type == "blockquote" for x in root_node.children)

    # find it and assert it matches
    quoted_text = to_text(quoted_content)
    sub_text = to_text(sub_content)
    for node in root_node.children:
        if node.type == "blockquote":
            # check the quoted part is quoted
            assert render_node(node) == quoted_text
            # check the content is not
            assert render_node(node.children[0]) == sub_text


def test_paragraph_node() -> None:
    test_data = [
        "# Heading",
        "paragraph content.",
        "second paragraph content.",
        "## second heading",
        "third paragraph content.",
    ]
    document = "\n\n".join(test_data)
    tree = parse_text_to_syntax_tree(document)
    
    tree_rep = tree.pretty()
    assert len(tree.children) == 5, tree_rep


def test_yes_no() -> None:
    assert parse_yes_no("yes")
    assert parse_yes_no("YES")
    assert not parse_yes_no("no")
    assert not parse_yes_no("No")
    assert parse_yes_no("Red") is None


def test_get_text_from_node() -> None:
    """Tests the get_text_from_node function, verifying it returns the text or code as a string."""

    # test basic text
    node = parse_text_to_syntax_tree("Some content")
    assert get_text_from_node(node) == "Some content"

    # test text with some emphasis
    node = parse_text_to_syntax_tree("Some _italic_ and **bold** content")
    # TODO: can we get this function to use spaces, not newlines, between style nodes?
    assert get_text_from_node(node) == "Some\nitalic\nand\nbold\ncontent"

    # test header
    node = parse_text_to_syntax_tree("# Some header")
    assert get_text_from_node(node) == "Some header"

    # test some inline code content
    node = parse_text_to_syntax_tree("Some `inline code;` snippet.")
    # TODO: can we get this function to use spaces, not newlines, between code and non-code nodes?
    assert get_text_from_node(node) == "Some\n`inline code;`\nsnippet."

    # test a code block
    node = parse_text_to_syntax_tree("    code block():")
    # TODO: fix this
    #assert get_text_from_node(node) == "code block():"


def test_check_node_is() -> None:
    # (node: SyntaxTreeNode, type_name: str, message: str) -> None:
    tree = parse_text_to_syntax_tree("Simple paragraph")
    node = tree.children[0]

    try:
        check_node_is(node, "paragraph")
    except IndexError:
        assert False, "paragraph node not identified"
    else:
        assert True

    # with message
    with pytest.raises(IndexError) as the_error:
        assert check_node_is(node, "bullet", "not a bullet")
    assert "not a bullet" in str(the_error)

    #without message
    with pytest.raises(IndexError) as the_error:
        assert check_node_is(node, "bullet")
    assert "not a bullet" not in str(the_error)

    

def test_list_item_parts() -> None:
    #(node: SyntaxTreeNode) -> list[SyntaxTreeNode] | None:
    pass
def test_split_list_item() -> None:
    #(node: SyntaxTreeNode) -> tuple[str, str]:
    pass
def test_read_bullet_list() -> None:
    bullet_list_content = "\n".join((
        f"- item {i}" for i in range(4)
        ))

    bullet_tree = parse_text_to_syntax_tree(bullet_list_content)

    assert bullet_tree.type == "root"

    bullet_list_node = bullet_tree.children[0]
    assert bullet_list_node.type == "bullet_list"

    bullet_list_items = read_bullet_list(bullet_list_node)

    with pytest.raises(TypeError) as the_error:
        root_response = read_bullet_list(bullet_tree)
    assert "Node is wrong type" in str(the_error)


def test_read_titled_bullet_list() -> None:
    titled_bullet_list_content = "\n".join((
        f"- **Title{i}:** item {i}" for i in range(4)
        ))

    titled_bullet_tree = parse_text_to_syntax_tree(titled_bullet_list_content)

    assert titled_bullet_tree.type == "root"

    titled_bullet_list_node = titled_bullet_tree.children[0]
    assert titled_bullet_list_node.type == "bullet_list"

    titled_bullet_list_items = read_titled_bullet_list(titled_bullet_list_node)

    with pytest.raises(TypeError) as the_error:
        root_response = read_titled_bullet_list(titled_bullet_tree)
    assert "Node is wrong type" in str(the_error)
