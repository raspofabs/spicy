"""Render any issues found with the collection of specs and use-cases."""

import logging
from collections.abc import Callable
from functools import partial

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


def render_issues(  # noqa: C901
    specs: list[SpecElement],
    use_cases: list[UseCase],
    render_function: Callable | None = None,
) -> bool:
    """Render unresolved issues for each use-case."""
    render_function = render_function or print
    any_errors = False
    for spec in specs:
        for issue in spec.get_issues():
            render_function(issue)
            any_errors = True
    for use_case in use_cases:
        for issue in use_case.get_issues():
            render_function(issue)
            any_errors = True
    if not any_errors:
        render_function("No issues found.")

    def just(checked_class: type) -> Callable:
        return partial(filter, lambda x: isinstance(x, checked_class))

    # check all use cases are connected to at least one stakeholder need
    stakeholder_needs = list(just(StakeholderNeed)(specs))
    logger.info("Have %s stakeholder needs", len(stakeholder_needs))

    stakeholder_needs_names = {n.name for n in stakeholder_needs}
    for use_case in use_cases:
        if not use_case.fulfils():
            render_function(f"Use case {use_case.name} fulfils nothing ({use_case.fulfils()}).")
        if disconnected := set(use_case.fulfils()) - stakeholder_needs_names:
            render_function(f"Use case {use_case.name} fulfils unexpected need {disconnected}.")

    # check all stakeholder needs are refined into at least one stakeholder requirements
    stakeholder_reqs = list(just(StakeholderRequirement)(specs))
    logger.info("Have %s stakeholder requirements", len(stakeholder_reqs))

    for stk_req in stakeholder_reqs:
        if not stk_req.fulfils():
            render_function(f"Stakeholder requirement {stk_req.name} fulfils nothing ({stk_req.fulfils()}).")
        if disconnected := set(stk_req.fulfils()) - stakeholder_needs_names:
            render_function(f"Stakeholder requirement {stk_req.name} fulfils unexpected need {disconnected}.")
    # check all stakeholder requirements are fulfilled by at least one system requirement
    system_reqs = list(just(SystemRequirement)(specs))
    logger.info("Have %s system requirements", len(system_reqs))

    # check all system requirements are captured by at least one system element
    system_elements = list(just(SystemElement)(specs))
    logger.info("Have %s system elements", len(system_elements))

    # check all system elements which are software elements derive to at least one software requirement
    software_requirements = list(just(SoftwareRequirement)(specs))
    logger.info("Have %s software requirements", len(software_requirements))

    # check all software requirements are satisfied by at least one software component
    software_components = list(just(SoftwareComponent)(specs))
    logger.info("Have %s software components", len(software_components))

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
