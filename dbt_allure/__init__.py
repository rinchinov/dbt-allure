import logging
import traceback

from allure_commons.logger import AllureFileLogger  # type: ignore
from allure_commons.model2 import (  # type: ignore
    TestResult,
)
from allure_commons.utils import uuid4  # type: ignore
from dbt.cli.main import EventMsg

from dbt_allure import utils
from dbt_allure.configs import ALLURE_CONFIGS

allure_logger = AllureFileLogger(
    report_dir=ALLURE_CONFIGS.get("results_dir"),
    clean=ALLURE_CONFIGS.get("clean_results")
)


class DBTAllure:
    manifest = None

    @classmethod
    def callback(cls, event: EventMsg) -> None:
        if event.info.name == "NewConnection" and cls.manifest is None:
            cls.manifest = "to do load manifest"
        if event.info.name == "NodeFinished" \
                and event.data.node_info.resource_type == "test":
            try:
                test_case = cls.convert_test_result_to_allure_test_case(event)
                allure_logger.report_result(test_case)
            except Exception as e:
                logging.error(f"allure test result parsing error {e}: traceback: {traceback.format_exc()}")

    @classmethod
    def convert_test_result_to_allure_test_case(cls, test_result: EventMsg) -> TestResult:
        timings = utils.get_node_timings(test_result.data.node_info)
        status = utils.get_node_status(test_result)
        links = utils.get_links(test_result)
        labels = utils.get_labels(test_result.info)
        steps = utils.get_steps(test_result)
        title = utils.get_title(test_result.data.node_info)
        return TestResult(
            uuid=uuid4(),
            historyId=test_result.data.node_info.unique_id,
            testCaseId=test_result.data.node_info.unique_id,
            fullName=test_result.data.node_info.node_name,
            name=title,
            links=links,
            labels=labels,
            status=status,
            steps=steps,
            **timings
        )
