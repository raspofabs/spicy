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


def render_issues(
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
    any_errors |= render_use_case_linkage_issues(specs, use_cases, render_function)
    any_errors |= render_stakeholder_requirement_linkage_issues(specs, render_function)
    any_errors |= render_system_requirement_linkage_issues(specs, render_function)
    any_errors |= render_system_element_linkage_issues(specs, render_function)
    any_errors |= render_software_componnet_linkage_issues(specs, render_function)
    any_errors |= render_software_unit_linkage_issues(specs, render_function)
    return any_errors


def render_use_case_linkage_issues(
    specs: list[SpecElement],
    use_cases: list[UseCase],
    render_function: Callable,
) -> bool:
    """Check all use cases are connected to at least one stakeholder need."""
    any_errors = False
    stakeholder_needs = list(just(StakeholderNeed)(specs))
    logger.info("Have %s stakeholder needs", len(stakeholder_needs))

    stakeholder_needs_names = {n.name for n in stakeholder_needs}
    unused_needs = set(stakeholder_needs_names)

    for use_case in use_cases:
        fulfilment = set(use_case.fulfils())
        if not fulfilment:
            any_errors = True
            render_function(f"Use case {use_case.name} fulfils nothing ({fulfilment}).")
        if disconnected := fulfilment - stakeholder_needs_names:
            any_errors = True
            render_function(f"Use case {use_case.name} fulfils unexpected need {disconnected}.")
        unused_needs = unused_needs - fulfilment

    if unused_needs:
        any_errors = True
        render_function(f"Needs without a use-case: {unused_needs}")
    return any_errors


def render_stakeholder_requirement_linkage_issues(
    specs: list[SpecElement],
    render_function: Callable,
) -> bool:
    """Check all stakeholder needs are refined into at least one stakeholder requirement."""
    any_errors = False
    stakeholder_reqs = list(just(StakeholderRequirement)(specs))
    stakeholder_needs = list(just(StakeholderNeed)(specs))
    logger.info("Have %s stakeholder requirements", len(stakeholder_reqs))

    stakeholder_needs_names = {n.name for n in stakeholder_needs}
    unrefined_needs = set(stakeholder_needs_names)

    for stk_req in stakeholder_reqs:
        fulfilment = set(stk_req.fulfils())
        if not fulfilment:
            any_errors = True
            render_function(f"Stakeholder requirement {stk_req.name} fulfils nothing ({fulfilment}).")
        if disconnected := fulfilment - stakeholder_needs_names:
            any_errors = True
            render_function(f"Stakeholder requirement {stk_req.name} fulfils unexpected need {disconnected}.")
        unrefined_needs = unrefined_needs - fulfilment

    if unrefined_needs:
        any_errors = True
        render_function(f"Needs without a stakeholder requirement: {unrefined_needs}")
    return any_errors


def render_system_requirement_linkage_issues(
    specs: list[SpecElement],
    render_function: Callable,
) -> bool:
    """Check all stakeholder requirements are fulfilled by at least one system requirement."""
    any_errors = False
    stakeholder_reqs = list(just(StakeholderRequirement)(specs))
    system_reqs = list(just(SystemRequirement)(specs))
    logger.info("Have %s system requirements", len(system_reqs))

    stakeholder_reqs_names = {n.name for n in stakeholder_reqs}
    unrefined_reqs = set(stakeholder_reqs_names)

    for sys_req in system_reqs:
        fulfilment = set(sys_req.fulfils())
        if not fulfilment:
            any_errors = True
            render_function(f"Stakeholder requirement {sys_req.name} fulfils nothing.")
        if disconnected := fulfilment - stakeholder_reqs_names:
            any_errors = True
            render_function(f"Stakeholder requirement {sys_req.name} fulfils unexpected need {disconnected}.")
        unrefined_reqs = unrefined_reqs - fulfilment

    if unrefined_reqs:
        any_errors = True
        render_function(f"Stakeholder reqs without a system requirement: {unrefined_reqs}")
    return any_errors


def render_system_element_linkage_issues(
    specs: list[SpecElement],
    _render_function: Callable,
) -> bool:
    """Check all system requirements are captured by at least one system element."""
    any_errors = False
    system_elements = list(just(SystemElement)(specs))
    logger.info("Have %s system elements", len(system_elements))
    return any_errors


def render_software_requirement_linkage_issues(
    specs: list[SpecElement],
    _render_function: Callable,
) -> bool:
    """Check all system elements which are software elements derive to at least one software requirement."""
    any_errors = False
    software_requirements = list(just(SoftwareRequirement)(specs))
    logger.info("Have %s software requirements", len(software_requirements))
    return any_errors


def render_software_componnet_linkage_issues(
    specs: list[SpecElement],
    _render_function: Callable,
) -> bool:
    """Check all software requirements are satisfied by at least one software component."""
    any_errors = False
    software_components = list(just(SoftwareComponent)(specs))
    logger.info("Have %s software components", len(software_components))
    return any_errors


def render_software_unit_linkage_issues(
    _specs: list[SpecElement],
    _render_function: Callable,
) -> bool:
    """Render unresolved use-case linkage issues."""
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
    return False


def just(checked_class: type) -> Callable:
    """Return a function which filters by checked_class."""
    return partial(filter, lambda x: isinstance(x, checked_class))
