"""Use case specific constants and utility functions."""

from spicy.md_read import SyntaxTreeNode, split_list_item

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
