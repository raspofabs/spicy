"""Construct SpecElements as they are read."""

import logging
from pathlib import Path

from spicy.use_cases.mappings import tcl_map

from .spec_utils import expected_links_for_variant, section_name_to_key
from .use_case_constants import section_map, usage_section_map

logger = logging.getLogger(__name__)


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

        self.qualification_related: bool | None = None
        self.software_requirement: bool | None = None

        self.title = ""
        self.content: dict[str, list[str]] = {}
        self.impact: str | None = None
        self.detectability: str | None = None
        self.usage_sections: dict[str, str] = {}

    @property
    def all_content(self) -> str:
        """Get all the content, comma separated."""
        return ", ".join((f"{k}:{v}" for k, v in self.content.items()))

    def __str__(self) -> str:
        """Return the string representation of the spec."""
        return " ".join(
            (
                f"{self.variant}:{self.name}({self.file_path}:{self.ordering_id})",
                f"{self.title} ({len(self.content)})[[{self.all_content}]]",
            ),
        )

    def get_linked_by(self, linkage_term: str) -> list[str]:
        """Return a list of all specs linked by this term."""
        link_content = self.content.get(linkage_term)
        if isinstance(link_content, list):
            return link_content
        if link_content is not None:
            logger.warning("No list content for %s - got [%s] instead", linkage_term, link_content)
        return []

    @property
    def is_qualification_related(self) -> bool:
        """Return whether this need has been marked as qualification related."""
        # All use-cases are qualification relevant if they are TCL2 or TCL3
        if self.variant == "UseCase":
            return self.tcl in ["TCL2", "TCL3"]

        # All requirements and design specs are optionally qualification related
        if self.qualification_related is not None:
            return self.qualification_related
        return False

    @property
    def is_software_element(self) -> bool:
        """Return whether this element requires software traceability."""
        # by default, we assume all requirements lead to software
        if self.software_requirement is None:
            return True
        return self.software_requirement

    def verification_criteria(self) -> list[str]:
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
        # check we have the minimum linkage
        issues = []
        required_links = expected_links_for_variant(self.variant)
        for link, target in required_links:
            link_key = section_name_to_key(link) or link
            if not self.get_linked_by(link_key):
                issues.append(f"Missing links for [{link} {target}]")

        if issues:
            issues = [f"{self.variant}({self.name}):", *issues]
        return issues

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
            issues.append(f"{len(no_section)} no section information for:{','.join(no_section)}")

        if issues:
            issues = [f"Issues in {self.file_path.name}, {self.name}", *issues]
        return issues

    @property
    def tcl(self) -> str | None:
        """Return the tcl class based on the tool impact and error detectability."""
        return tcl_map(self.impact, self.detectability)
