"""Create a TDP from the documentation."""

import logging
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path

from .mappings import tcl_map

logger = logging.getLogger("UseCases")

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


class UseCase:
    """Gather information on use-cases and feedback on missing elements."""

    def __init__(  # noqa: PLR0913 - only the dedicated builder object builds this.
        self,
        name: str,
        ordering_id: int,
        file_path: Path,
        title: str,
        content: defaultdict[str, list[str]],
        impact: str | None,
        detectability: str | None,
        usage_sections: dict[str, str],
        needs_fulfilled: list[str],
    ) -> None:
        """Construct the basic properties."""
        self.name = name
        self.ordering_id = ordering_id
        self.file_path = file_path
        self.title = title
        self.content = content
        self.impact = impact
        self.detectability = detectability
        self.usage_sections = usage_sections
        self.fulfils_needs = needs_fulfilled

    @property
    def tcl(self) -> str | None:
        """Return the tcl class based on the tool impact and error detectability."""
        return tcl_map(self.impact, self.detectability)

    def fulfils(self) -> list[str]:
        """Return a list of all the needs this use-case fulfils."""
        return self.fulfils_needs

    def render_issues(self, render_function: Callable) -> bool:
        """Render issues with missing properties."""
        issues = self.get_issues()
        if issues:
            render_function(f"Issues in {self.file_path.name}, {self.name}")
            for issue in issues:
                render_function(f"\t{issue}")
            return True
        return False

    def get_issues(self) -> list[str]:
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

        return issues

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
