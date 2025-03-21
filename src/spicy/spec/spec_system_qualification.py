"""System qualification test spec element."""

import logging
from pathlib import Path

from spicy.md_read import SyntaxTreeNode, get_text_from_node, read_bullet_list

from .spec_element import SpecElement

logger = logging.getLogger(__name__)


class SystemQualificationTest(SpecElement):
    """Handles system QualificationTests parsing."""

    def __init__(self, name: str, ordering: int, from_file: Path) -> None:
        """Construct super and placeholder fields."""
        super().__init__(name, ordering, from_file, spec_type="System qualification test")
        self.content: list[str] = []
        self.tests_list: list[str] = []
        self.cases_list: list[str] = []
        self.results_list: list[str] = []
        self.state = ""
        self.spec_prefix, __ = name.split("_SYS_QUAL_")

    def tests(self) -> list[str]:
        """Return a list of names of system requirements this system qualification test tests."""
        return self.tests_list

    def monitors(self) -> list[str]:
        """Return a list of names of test cases this system qualification test depends on."""
        return self.cases_list

    @staticmethod
    def is_spec_heading(header_text: str) -> bool:
        """Return whether the header_node relates to this class of spec."""
        # e.g. CDU_SYS_REQ_1_1_cookie_ordering
        return "_SYS_QUAL_" in header_text

    def parse_node(self, node: SyntaxTreeNode) -> None:
        """Parse a SyntaxTreeNode."""
        logger.debug("Parsing as system qualification test: %s", node.pretty(show_text=True))
        if get_text_from_node(node) == "Tests:":
            self.state = "reqs_list"
        if node.type == "bullet_list" and self.state == "reqs_list":
            tested_reqs = read_bullet_list(node)
            self.tests_list.extend([get_text_from_node(x) for x in tested_reqs])
            self.state = ""
        if get_text_from_node(node) == "Cases:":
            self.state = "cases_list"
        if node.type == "bullet_list" and self.state == "cases_list":
            test_cases = read_bullet_list(node)
            self.cases_list.extend([get_text_from_node(x) for x in test_cases])
            self.state = ""
        if get_text_from_node(node) == "Results:":
            self.state = "results_list"
        if node.type == "bullet_list" and self.state == "results_list":
            results = read_bullet_list(node)
            self.results_list.extend([get_text_from_node(x) for x in results])
            self.state = ""

    def get_issues(self) -> list[str]:
        """Get issues with this spec."""
        issues = []
        if not self.tests_list:
            issues.append("Does not test any system requirements.")
        if not self.cases_list:
            issues.append("Does not monitor any test cases.")
        else:
            test_spec_name_prefix = self.spec_prefix+"_SYS_TEST_"
            badly_named_tests = [case for case in self.cases_list if not case.startswith(test_spec_name_prefix)]
            if badly_named_tests:
                issues.append(f"Not all tests are correctly named: {badly_named_tests}")
        if not self.results_list:
            issues.append("Does not have any test results.")
        else:
            result_tests = [result.split(":")[0] for result in self.results_list]
            unlinked_results = [result for result in result_tests if result not in self.cases_list]
            if unlinked_results:
                issues.append(f"Not all results are correctly named: {unlinked_results}")
            cases_without_results = set(self.cases_list) - set(result_tests)
            if cases_without_results:
                issues.append(f"Not all test cases have results : {list(cases_without_results)}")
        if issues:
            issues = [f"SystemQualificationTest({self.name}):", *issues]
        return issues
