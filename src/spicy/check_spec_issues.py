"""Render any issues found with the collection of specs and use-cases."""

import logging
from functools import partial
from typing import Any, Callable, List, Optional

from .spec import SpecElement
from .spec.builder import (
    SoftwareComponent,
    SoftwareRequirement,
    StakeholderNeed,
    StakeholderRequirement,
    SystemElement,
    SystemRequirement,
)
from .use_cases import UseCase

logger = logging.getLogger(__name__)


def render_issues(specs: List[SpecElement], use_cases: List[UseCase], render_function: Optional[Callable] = None):
    """Render unresolved issues for each use-case."""
    render_function = render_function or print
    any_errors = False
    for spec in specs:
        if spec.render_issues(render_function):
            any_errors = True
    for use_case in use_cases:
        if use_case.render_issues(render_function):
            any_errors = True
    if not any_errors:
        render_function("No issues found.")

    def just(checked_class: Any):
        return partial(filter, lambda x: isinstance(x, checked_class))

    # check all use cases are connected to at least one stakeholder need
    stakeholder_needs = list(just(StakeholderNeed)(specs))
    logger.info(f"Have {len(stakeholder_needs)} stakeholder needs")

    stakeholder_needs_names = {n.name for n in stakeholder_needs}
    for use_case in use_cases:
        if not use_case.fulfils():
            render_function(f"Use case {use_case.name} fulfils nothing ({use_case.fulfils()}).")
        if disconnected := set(use_case.fulfils()) - stakeholder_needs_names:
            render_function(f"Use case {use_case.name} fulfils unexpected need {disconnected}.")
        # if not any(use_case in stk_need.use_cases() for stk_need in stakeholder_needs):
        # print(f"Use case {use_case.name} is not needed.")

    # check all stakeholder needs are refined into at least one stakeholder requirements
    stakeholder_reqs = list(just(StakeholderRequirement)(specs))
    logger.info(f"Have {len(stakeholder_reqs)} stakeholder requirements")
    # check all stakeholder requirements are fulfilled by at least one system requirement
    system_reqs = list(just(SystemRequirement)(specs))
    logger.info(f"Have {len(system_reqs)} system requirements")
    # check all system requirements are captured by at least one system element
    system_elements = list(just(SystemElement)(specs))
    logger.info(f"Have {len(system_elements)} system elements")
    # check all system elements which are software elements derive to at least one software requirement
    software_requirements = list(just(SoftwareRequirement)(specs))
    logger.info(f"Have {len(software_requirements)} software requirements")
    # check all software requirements are satisfied by at least one software component
    software_components = list(just(SoftwareComponent)(specs))
    logger.info(f"Have {len(software_components)} software components")
    # check all software components have at least one software unit design
    # check all software units have at least one unit test
    # check all software components have integration tests
    # check all software requirements have qualification tests
    # check all system elements have integration tests
    # check all system requirements have system qualification tests

    # bidirectional traceability does not require that all elements are
    # bi-directionally dependent, only that any stakeholder needs must be
    # traceable back and forth. Additional tests, software components, even
    # software requirements, can be introduced with rationale not originating
    # from the stakeholder needs.

    return any_errors
