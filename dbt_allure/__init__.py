import logging
import traceback

from allure_commons.logger import AllureFileLogger  # type: ignore
from dbt.cli.main import EventMsg

from dbt_allure.configs import ALLURE_CONFIGS
from dbt_allure.parse import convert_test_result_to_allure_test_case

allure_logger = AllureFileLogger(
    report_dir=ALLURE_CONFIGS.get("results_dir"),
    clean=ALLURE_CONFIGS.get("clean_results")
)


def allure_callback(event: EventMsg) -> None:
    if event.info.name == "NodeFinished" \
            and event.data.node_info.resource_type == "test":
        try:
            test_case = convert_test_result_to_allure_test_case(event)
            allure_logger.report_result(test_case)
        except Exception as e:
            logging.error(f"allure test result parsing error {e}: traceback: {traceback.format_exc()}")
