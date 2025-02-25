from spicy.md_read import list_item_parts, load_syntax_tree, parse_text_to_syntax_tree


def test_load_markdown_to_syntax_tree(test_data_path):
    node = load_syntax_tree(test_data_path / "use_cases" / "01_simple_valid.md")
    assert node is not None


def test_list_item_parts():
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
