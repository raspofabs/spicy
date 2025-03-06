from typing import List

from spicy.md_read import list_item_parts, load_syntax_tree, parse_text_to_syntax_tree, render_node


def test_load_markdown_to_syntax_tree(test_data_path):
    """Test a simple md file load and parse."""
    node = load_syntax_tree(test_data_path / "use_cases" / "01_simple_valid.md")
    assert node is not None


def test_list_item_parts():
    """Test parsing of list items."""
    root_node = parse_text_to_syntax_tree("- **title:** text content `inline code` more text.")
    print(root_node.pretty(indent=2, show_text=True))
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


def test_read_and_re_render():
    """Test the ability to write out what we read."""

    def to_text(lines: List[str]) -> str:
        return "\n".join(lines + [""])

    sub_content = ["I like to have", "Some quoted text.", "-- me."]
    quoted_content = ["> " + line for line in sub_content]
    test_content = ["#Title", "", "This is some content.", ""] + quoted_content + ["", "Last content."]
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
