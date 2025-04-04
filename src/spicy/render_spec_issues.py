"""Render any issues found with the collection of specs and use-cases."""

import logging
from collections import Counter
from collections.abc import Callable
from functools import partial

from .spec import SpecElement
from .spec.builder import (
    SoftwareComponent,
    SoftwareRequirement,
    StakeholderNeed,
    StakeholderRequirement,
    SystemElement,
    SystemIntegrationTest,
    SystemQualificationTest,
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

    for spec_name, count in Counter(x.name for x in specs).items():
        if count > 1:
            render_function(f"Non unique name {spec_name} has {count} instances")

    # SYS.1 -> Tool Qualification
    any_errors |= render_use_case_linkage_issues(specs, use_cases, render_function)

    # SYS.1 -> SYS.1
    any_errors |= render_stakeholder_requirement_linkage_issues(specs, render_function)

    # SYS.1 -> SYS.2
    any_errors |= render_system_requirement_linkage_issues(specs, render_function)

    # SYS.2 -> SYS.3
    any_errors |= render_system_element_linkage_issues(specs, render_function)

    # SYS.3 -> SWE.1
    any_errors |= render_software_requirement_linkage_issues(specs, render_function)

    # SWE.1 -> SWE.2
    any_errors |= render_software_component_linkage_issues(specs, render_function)

    # SWE.2 -> SWE.3
    any_errors |= render_software_unit_linkage_issues(specs, render_function)

    # SWE.2 -> SWE.5
    any_errors |= render_software_integration_linkage_issues(specs, render_function)

    # SWE.1 -> SWE.6
    any_errors |= render_software_qualification_linkage_issues(specs, render_function)

    # SYS.3 -> SWE.4
    any_errors |= render_system_integration_linkage_issues(specs, render_function)

    # SYS.2 -> SWE.5
    any_errors |= render_system_qualification_linkage_issues(specs, render_function)

    if not any_errors:
        render_function("No spec issues found.")
    return any_errors


def render_use_case_linkage_issues(
    specs: list[SpecElement],
    use_cases: list[UseCase],
    render_function: Callable,
) -> bool:
    """Check all use cases are connected to at least one stakeholder need."""
    any_errors = False

    stakeholder_needs = list(just(StakeholderNeed)(specs))
    logger.debug("Have %s stakeholder needs", len(stakeholder_needs))

    stakeholder_needs_map = {n.name: n for n in stakeholder_needs}
    stakeholder_needs_names = set(stakeholder_needs_map.keys())
    unused_needs = set(stakeholder_needs_names)

    for use_case in use_cases:
        fulfilment = set(use_case.fulfils())
        if use_case.safety_case:
            uc_needs: list[SpecElement] = list(filter(None, [stakeholder_needs_map.get(a) for a in fulfilment]))
            if not any(need.is_safety_related for need in uc_needs):
                any_errors = True
                render_function(f"Use case {use_case.name} is safety related, but none of it's needs are:")
                for need in uc_needs:
                    render_function(f"\t{need.name}")

        if disconnected := fulfilment - stakeholder_needs_names:
            any_errors = True
            render_function(f"Use case {use_case.name} fulfils unexpected need {disconnected}.")
        unused_needs = unused_needs - fulfilment

    if unused_needs:
        any_errors = True
        render_function("Needs without a use-case:")
        for need in sorted(unused_needs):
            render_function(f"\t{need}")

    return any_errors


def render_stakeholder_requirement_linkage_issues(
    specs: list[SpecElement],
    render_function: Callable,
) -> bool:
    """Check all stakeholder needs are refined into at least one stakeholder requirement."""
    any_errors = False
    stakeholder_reqs = list(just(StakeholderRequirement)(specs))
    stakeholder_needs = list(just(StakeholderNeed)(specs))
    logger.debug("Have %s stakeholder requirements", len(stakeholder_reqs))

    stakeholder_needs_names = {n.name for n in stakeholder_needs}
    unfulfilled_needs = set(stakeholder_needs_names)

    for stk_req in stakeholder_reqs:
        fulfilment = set(stk_req.fulfils())
        if disconnected := fulfilment - stakeholder_needs_names:
            any_errors = True
            render_function(f"Stakeholder requirement {stk_req.name} fulfils unexpected need {disconnected}.")
        unfulfilled_needs = unfulfilled_needs - fulfilment

    if unfulfilled_needs:
        any_errors = True
        render_function("Needs without a fulfilling stakeholder requirement:")
        for need in sorted(unfulfilled_needs):
            render_function(f"\t{need}")

    for need in stakeholder_needs:
        result, messages = check_safety(need, stakeholder_reqs, lambda x: x.fulfils())
        any_errors |= result
        for m in messages:
            render_function(m)

    return any_errors


def render_system_requirement_linkage_issues(
    specs: list[SpecElement],
    render_function: Callable,
) -> bool:
    """Check all stakeholder requirements are fulfilled by at least one system requirement."""
    any_errors = False
    stakeholder_reqs = list(just(StakeholderRequirement)(specs))
    system_reqs = list(just(SystemRequirement)(specs))
    logger.debug("Have %s system requirements", len(system_reqs))

    stakeholder_reqs_names = {n.name for n in stakeholder_reqs}
    unrefined_stk_reqs = set(stakeholder_reqs_names)

    for sys_req in system_reqs:
        fulfilment = set(sys_req.fulfils())
        if disconnected := fulfilment - stakeholder_reqs_names:
            any_errors = True
            render_function(f"System requirement {sys_req.name} fulfils unexpected need {disconnected}.")
        unrefined_stk_reqs = unrefined_stk_reqs - fulfilment

    if unrefined_stk_reqs:
        any_errors = True
        render_function("Stakeholder requirements without a system requirement:")
        for unrefined_stk_req in sorted(unrefined_stk_reqs):
            render_function(f"\t{unrefined_stk_req}")

    for stk_req in stakeholder_reqs:
        result, messages = check_safety(stk_req, system_reqs, lambda x: x.fulfils())
        any_errors |= result
        for m in messages:
            render_function(m)

    return any_errors


def render_system_element_linkage_issues(
    specs: list[SpecElement],
    render_function: Callable,
) -> bool:
    """Check all system requirements are captured by at least one system element."""
    any_errors = False
    system_reqs = list(just(SystemRequirement)(specs))
    system_elements = list(just(SystemElement)(specs))
    logger.debug("Have %s system elements", len(system_elements))

    system_req_names = {n.name for n in system_reqs}
    unsatisfied_system_reqs = set(system_req_names)

    for sys_element in system_elements:
        fulfilment = set(sys_element.fulfils())
        if disconnected := fulfilment - system_req_names:
            any_errors = True
            render_function(f"System requirement {sys_element.name} fulfils unexpected need {disconnected}.")
        unsatisfied_system_reqs = unsatisfied_system_reqs - fulfilment

    if unsatisfied_system_reqs:
        any_errors = True
        render_function("System requirements without a system element:")
        for unrefined_stk_req in sorted(unsatisfied_system_reqs):
            render_function(f"\t{unrefined_stk_req}")
    return any_errors


def render_software_requirement_linkage_issues(
    specs: list[SpecElement],
    render_function: Callable,
) -> bool:
    """Check all system elements which are software elements derive to at least one software requirement."""
    any_errors = False
    system_elements = list(just(SystemElement)(specs))
    software_requirements = list(just(SoftwareRequirement)(specs))
    logger.debug("Have %s software requirements", len(software_requirements))

    system_element_names = {n.name for n in system_elements if n.is_software_element()}
    unrefined_system_elements = set(system_element_names)

    for sw_req in software_requirements:
        fulfilment = set(sw_req.fulfils())
        if disconnected := fulfilment - system_element_names:
            any_errors = True
            render_function(f"Software requirement {sw_req.name} refined from unexpected element {disconnected}.")
        unrefined_system_elements = unrefined_system_elements - fulfilment

    if unrefined_system_elements:
        any_errors = True
        render_function("System software elements without software requirements:")
        for unrefined_stk_req in sorted(unrefined_system_elements):
            render_function(f"\t{unrefined_stk_req}")
    return any_errors


def render_software_component_linkage_issues(
    specs: list[SpecElement],
    _render_function: Callable,
) -> bool:
    """Check all software requirements are satisfied by at least one software component."""
    any_errors = False
    software_components = list(just(SoftwareComponent)(specs))
    logger.debug("Have %s software components", len(software_components))
    return any_errors


def render_software_integration_linkage_issues(
    specs: list[SpecElement],
    _render_function: Callable,
) -> bool:
    """Check all software components have integration tests."""
    any_errors = False
    software_components = list(just(SoftwareComponent)(specs))
    logger.debug("Have %s software components", len(software_components))
    return any_errors


def render_software_qualification_linkage_issues(
    specs: list[SpecElement],
    _render_function: Callable,
) -> bool:
    """Check all software requirements have qualification tests."""
    any_errors = False
    software_components = list(just(SoftwareComponent)(specs))
    logger.debug("Have %s software components", len(software_components))
    return any_errors


def render_software_unit_linkage_issues(
    _specs: list[SpecElement],
    _render_function: Callable,
) -> bool:
    """Check all software components have at least one software unit design."""
    return False


def render_system_integration_linkage_issues(
    specs: list[SpecElement],
    render_function: Callable,
) -> bool:
    """Check all system elements have integration tests."""
    any_errors = False
    system_elements = list(just(SystemElement)(specs))
    system_integration_tests = list(just(SystemIntegrationTest)(specs))
    logger.debug("Have %s system integration tests", len(system_integration_tests))

    system_element_names = {n.name for n in system_elements}
    untested_integrations = set(system_element_names)

    for sys_int_test in system_integration_tests:
        fulfilment = set(sys_int_test.integrates())
        if disconnected := fulfilment - system_element_names:
            any_errors = True
            render_function(
                f"System integration test {sys_int_test.name} tests unexpected element {disconnected}.",
            )
        untested_integrations = untested_integrations - fulfilment

    if untested_integrations:
        any_errors = True
        render_function("System elements without any integration tests:")
        for untested_req in sorted(untested_integrations):
            render_function(f"\t{untested_req}")
    return any_errors


def render_system_qualification_linkage_issues(
    specs: list[SpecElement],
    render_function: Callable,
) -> bool:
    """Check all system requirements have system qualification tests."""
    any_errors = False
    system_reqs = list(just(SystemRequirement)(specs))
    system_qualification_tests = list(just(SystemQualificationTest)(specs))
    logger.debug("Have %s system qualification tests", len(system_qualification_tests))

    system_reqs_names = {n.name for n in system_reqs}
    untested_reqs = set(system_reqs_names)

    for sys_qual_test in system_qualification_tests:
        tested_list = set(sys_qual_test.tests())
        if disconnected := tested_list - system_reqs_names:
            any_errors = True
            render_function(
                f"System qualification test {sys_qual_test.name} tests unexpected requirement {disconnected}.",
            )
        untested_reqs = untested_reqs - tested_list

    if untested_reqs:
        any_errors = True
        render_function("System requirements without a qualification test:")
        for untested_req in sorted(untested_reqs):
            render_function(f"\t{untested_req}")

    for system_req in system_reqs:
        result, messages = check_safety(system_req, system_qualification_tests, lambda x: x.tests())
        any_errors |= result
        for m in messages:
            render_function(m)

    return any_errors


def just(checked_class: type) -> Callable:
    """Return a function which filters by checked_class."""
    return partial(filter, lambda x: isinstance(x, checked_class))


def check_safety(
    safe_spec: SpecElement,
    other_specs: list[SpecElement],
    fulfilment: Callable,
) -> tuple[bool, list[str]]:
    """Check and return whether there are safety linkage issues."""
    if not safe_spec.is_safety_related:
        return False, []
    relevant_specs = [spec for spec in other_specs if safe_spec.name in fulfilment(spec)]
    target = "safety related spec"
    if relevant_specs:
        spec, *__ = relevant_specs
        target = f"safety related {spec.__class__.__name__}"
    if any(x.is_safety_related for x in relevant_specs):
        return False, []
    # nothing safe connected
    messages = [f"{safe_spec.name} is not satisfied by any {target}"]
    messages.extend(f"\t{os.name}" for os in relevant_specs)
    return True, messages


# TODO @fabs: check all software units have at least one unit test - how? Need source access.


# bidirectional traceability does not require that all elements are
# bi-directionally dependent, only that any stakeholder needs must be
# traceable back and forth. Additional tests, software components, even
# software requirements, can be introduced with rationale not originating
# from the stakeholder needs.
