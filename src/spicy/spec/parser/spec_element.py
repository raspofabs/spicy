"""Construct SpecElements as they are read."""

import logging
from pathlib import Path

from spicy.use_cases.mappings import tcl_map
from .use_case_constants import section_map, usage_section_map


class SpecElement:
    """Spec Element class to store details of the spec element and links to other elements."""

    def __init__(
        self,
        name: str,
        variant: str,
        ordering_id: int,
        file_path: Path,
        *,
        links: dict[str, list[str]] | None = None,
    ) -> None:
        """Construct the basic properties."""
        self.name = name
        self.variant = variant
        self.ordering_id = ordering_id
        self.file_path = file_path

        self._qualification_related: bool | None = None
        self._links: dict[str, list[str]] = links or {}

        self.title = ""
        self.content: dict[str, list[str]] = {}
        self.impact: str | None = None
        self.detectability: str | None = None
        self.usage_sections: dict[str, str] = {}

    @property
    def all_content(self) -> str:
        return ", ".join((
            f"{k}:{v}" for k, v in self.content.items()))

    def __str__(self) -> str:
        return " ".join((
            f"{self.variant}:{self.name}({self.file_path}:{self.ordering_id})",
            f"{self.title} ({len(self.content)})[[{self.all_content}]]"
            ))

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

    def verification_criteria(self):
        """Return a list of qualification criteria."""
        return self.content.get("verification_criteria", [])

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


