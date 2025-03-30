"""System requirement spec element."""

import logging
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, get_text_from_node, read_bullet_list, read_titled_bullet_list

from .spec_element import SpecElement

logger = logging.getLogger(__name__)


class SystemRequirement(SpecElement):
    """Handles system requirements parsing."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="System Requirement")
        self.content: list[str] = []
        self.derived_from_list: list[str] = []
        self.verification_list: list[str] = []
        self.specification: dict[str, str] = {}
        self.state = ""

    def fulfils(self) -> list[str]:
        """Return a list of names of stakeholder requirements this system requirement resolves."""
        return self.derived_from_list

    @property
    def is_safety_related(self) -> bool:
        """Return whether the spec is safety related based on specification first."""
        if self.specification.get("safety related", "").lower().strip(".") == "yes":
            return True
        return super().is_safety_related

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SYS_REQ_1_1_cookie_ordering
        return "_SYS_REQ_" in header_text

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        super().parse_node(node)
        detail_heading = self.is_detail_heading(node)

        logger.debug("Parsing as system requirement: %s", node.pretty(show_text=True))
        if detail_heading == "derived from":
            self.state = "reqs_list"
        elif detail_heading == "verification criteria":
            self.state = "verification_list"
        elif detail_heading == "specification":
            self.state = "specification_list"

        if node.type == "code_block" and self.state == "reqs_list":
            reqs_list = [x.strip() for x in node.content.split("\n") if x.strip()]
            self.derived_from_list.extend(reqs_list)
            self.state = ""
        if node.type == "bullet_list":
            if self.state == "reqs_list":
                reqs_list = read_bullet_list(node)
                self.derived_from_list.extend([get_text_from_node(x) for x in reqs_list])
                self.state = ""
            if self.state == "verification_list":
                elements_list = read_bullet_list(node)
                self.verification_list.extend([get_text_from_node(x) for x in elements_list])
                self.state = ""
            if self.state == "specification_list":
                new_spec = {a.strip().strip(":").lower(): b.strip() for a, b in read_titled_bullet_list(node).items()}
                self.specification.update(new_spec)
                self.state = ""

    def get_issues(self) -> list[str]:
        """Get issues with this spec."""
        issues = []
        if not self.verification_list:
            issues.append("Has no verification criteria.")
        if not self.derived_from_list:
            issues.append("Does not derive from any stakeholder requirements.")
        if not self.specification:
            issues.append("Has no detailed specification.")
        if issues:
            issues = [f"SystemRequirement({self.name}):", *issues]
        return issues


# Look for verification criteria

# In a system requirement, look for a set of details:

# Specification:
#
# - **Requirement type:**
#   - business function, organisational function;
#   - user, safety, security, ergonomic, interface;
#   - operational, maintenance;
#   - design constraint;
#   - qualification
# - **Interaction:** system elements / software, nature of interaction
# - **Constraints:**
#   - resource limits;
#   - performance constraints;
#   - safety, security expectations;
#   - interface and API constraints
# - **Operational and environmental limits and capabilities:**
# - **Documentation:** where it is, what it is for.
# - **Safety related:** yes/no
# - **Auditable:** yes/no
#
# System requirements include: functions and capabilities of the system;
# business, organizational and user requirements; safety, security,
# human-factors engineering (ergonomics), interface, operations, and
# maintenance requirements; design constraints and qualification requirements.
# (ISO/IEC 12207)
#    - business requirements:
#        Such as requirement to achieve certain compliance level.
#        They are about what the system will need to do to resolve some lack in
#        what the business is capable of.
#        Think in terms of KPIs and goals.
#        These needs are likely to be less strict, easily prioritised, even optional.
#    - Organizatinoal requirements:
#        These can be things like the limit on the cost to deliver or the
#        availability of the implmementors or verifiers.
#        Constraints can include how and when the system works with existing processes.
#        Limitations can include the working environment and tools available.
#    - User requirement:
#        Requirements related to the users, such as their skills and strengths, weaknesses or deficiencies.
#        Requirements for the effectiveness of the solution system in terms of performance and maintainability.
#    - Safety and security requirements: related to safety and security
#    - Human-factors engineering (ergonomics): relates to the way which the system is used by humans.
#    - Interface requirements: what affordances it must have to external systems, e.g. document formats for delivery.
#    - Operations requirements:
#        Operations is about the running of the system.
#        These requirements can be about uptime, time to recovery, or updating procedures.
#        They can relate to logs, and the ability to rollback changes.
#        Observability might exist here.
#        Documentation on how to fix issues would be an operational requirement.
#        For some tools, it can include how to integrate into the existing infrastructure.
#    - Maintenance requirements:
#    - Design requirements:
#        These are requirements generally about the structure or implementation.
#        They can include decisions to use specific architectures, frameworks,
#        or approaches to resolving other problems or requirements.
#    - Qualification requirements:
#        Define the features that define whether the system is able to do its job
#        Characteristics, attributes, or properties of the system that must be
#        present, otherwise the system is not fit for purpose.
#        Examples include operational limits such as storage space,
#        temperature, or qualification measures such as whether it meets the
#        constraints of a development process of international standards
#        document for code-quality.
#
# Beyond this:
# - Identifies any relationship considerations / constraints between the system elements and the software
# - Identifies any interrelationship considerations / constraints between system elements
# - Identifies the required system overview
# - Identifies any design considerations / constraints for each required system element, including:
#     - memory / capacity requirements
#     - hardware interfaces requirements
#     - user interfaces requirements
#     - external system interface requirements
#     - performance requirements
#     - commands structures
#     - security / data protection characteristics
#     - application parameter settings
#     - manual operations
#     - reusable components
# - Describes the operation capabilities
# - Describes environmental capabilities
# - Documentation requirements
# - Reliability requirements
# - Logistical Requirements
# - Describes security requirements
# - Diagnosis requirements
