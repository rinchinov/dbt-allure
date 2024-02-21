import json
import traceback
import uuid
import os
from dbt.cli.main import EventMsg
from datetime import datetime, timezone
from dbt_allure.data import TestCase, Link, Label, Step
from dbt_allure import configuration
import logging


ALLURE_CONFIGS = configuration.get_configurations()
LINKS = (
    "tsm",
    "issue"
)
LABELS = (
    "severity",
    "owner",
    "epic",
    "feature",
    "story",
    "parentSuite",
    "suite",
    "subSuite",
    "package"
)
META_MAPPING = dict(
    title_key=os.environ.get("DBT_ALLURE_TITLE_KEY", "allure_title"),
    description_key=os.environ.get("DBT_ALLURE_TITLE_KEY", "allure_description"),
    owner_key=os.environ.get("DBT_ALLURE_OWNER_KEY", "allure_owners"),
    owner_default=os.environ.get("DBT_ALLURE_OWNER_DEFAULT", "Nobody"),
)


def to_milliseconds(seconds: int, nanos: int) -> int:
    return (seconds * 1000) + (nanos // 1_000_000)


def get_from_meta(meta, key, default):
    value = meta.get(key)
    if value:
        return value.string_value or value.number_value
    else:
        return default


def get_label_from_meta(meta, label_name):
    _key = META_MAPPING[label_name + "_key"]
    _default = META_MAPPING[label_name + "_default"]
    _value = get_from_meta(meta, _key, _default)
    if _value:
        return Label(name=label_name, value=_value)


def get_link_from_meta(meta, link_name):
    _key = META_MAPPING[link_name + "_key"]
    _default = META_MAPPING[link_name + "_default"]
    _link_template = META_MAPPING[link_name + "_template"]
    _value = get_from_meta(meta, _key, _default)
    if _value:
        return Link(
            type=link_name,
            name=link_name,
            url=_link_template.format(_value)
        )


def node_status(test_result):
    status = test_result.data.run_result.status
    if status == "pass":
        return "passed"
    else:
        return "failed"


def get_title(test_result):
    meta = test_result.data.node_info.meta.fields
    return get_from_meta(meta, META_MAPPING["title_key"], test_result.data.node_info.node_name)


def get_adapter_response(test_result):
    # adapter_response = get_adapter_response(test_result)

    """
    # for name, value in test_result.data.run_result.adapter_response.fields.items():
    #     steps.append(
    #         Step(
    #             name=f"{name}: {value}",
    #             status=status,
    #             start=int(start),
    #             stop=int(stop),
    #         )
    #     )
    """
    raise NotImplementedError


def get_links(test_result):
    """
    for link in LINKS:
    link = get_link_from_meta(meta, link)
    if link:
        links.append(link)
    """
    return []


def get_labels(test_result):
    """
    for label in LABELS:
        label = get_label_from_meta(meta, label)
        if label:
            labels.append(label)
    """
    return [
        Label(name="framework", value="dbt"),
        Label(name="language", value="SQL"),
        Label(name="resource_type", value=test_result.data.node_info.resource_type),
        Label(name="node_status", value=test_result.data.node_info.node_status),
        Label(name="invocation_id", value=test_result.info.invocation_id),
        Label(name="pid", value=test_result.info.pid),
        Label(name="thread", value=test_result.info.thread),
    ]


def get_steps(test_result):
    status = node_status(test_result)
    start = datetime.fromisoformat(test_result.data.node_info.node_started_at).replace(
        tzinfo=timezone.utc).timestamp() * 1000
    stop = datetime.fromisoformat(test_result.data.node_info.node_finished_at).replace(
        tzinfo=timezone.utc).timestamp() * 1000
    return [
        Step(
            name=test_result.data.run_result.message,
            status=status,
            start=int(start),
            stop=int(stop),
        ),
        Step(
            name=test_result.info.msg,
            status=status,
            start=int(start),
            stop=int(stop),
        ),
    ]


def convert_test_result_to_allure_test_case(test_result) -> TestCase:
    start = datetime.fromisoformat(test_result.data.node_info.node_started_at).replace(
        tzinfo=timezone.utc).timestamp() * 1000
    stop = datetime.fromisoformat(test_result.data.node_info.node_finished_at).replace(
        tzinfo=timezone.utc).timestamp() * 1000
    status = node_status(test_result)
    links = get_links(test_result)
    labels = get_labels(test_result)
    steps = get_steps(test_result)
    title = get_title(test_result)
    return TestCase(
        uuid=str(uuid.uuid4()),
        historyId=test_result.data.node_info.unique_id,
        testCaseId=test_result.data.node_info.unique_id,
        fullName=test_result.data.node_info.node_name,
        name=title,
        links=links,
        labels=labels,
        status=status,
        start=int(start),
        stop=int(stop),
        steps=steps
    )


def allure_callback(event: EventMsg) -> None:
    if event.info.name == "NodeFinished" \
            and event.data.node_info.resource_type == "test":
        try:
            test_case = convert_test_result_to_allure_test_case(event)
        except Exception as e:
            logging.error(f"allure test result parsing error {e}: traceback: {traceback.format_exc()}")
            return
        try:
            path = f"target/allure-results/"
            os.makedirs(path, exist_ok=True)
            with open(f"{path}/{test_case.uuid}-result.json", "w+") as f:
                json.dump(test_case.to_dict(), f)
        except Exception as e:
            logging.error(f"allure test result saving error {e}: traceback: {traceback.format_exc()}")
