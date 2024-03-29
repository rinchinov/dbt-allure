import os
from datetime import datetime, timezone

from allure_commons.model2 import (  # type: ignore
    Label,
    Link,
    TestStepResult,
)

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
META_MAPPING = {
    "title_key": os.environ.get("DBT_ALLURE_TITLE_KEY", "allure_title"),
    "description_key": os.environ.get("DBT_ALLURE_TITLE_KEY", "allure_description"),
    "owner_key": os.environ.get("DBT_ALLURE_OWNER_KEY", "allure_owners"),
    "owner_default": os.environ.get("DBT_ALLURE_OWNER_DEFAULT", "Nobody"),
}


def to_milliseconds(seconds: int, nanos: int) -> int:
    return (seconds * 1000) + (nanos // 1_000_000)


def get_from_meta(meta, key, default):
    value = meta.get(key)
    if value:
        return value.string_value or value.number_value
    return default


def get_label_from_meta(meta, label_name):
    _key = META_MAPPING[label_name + "_key"]
    _default = META_MAPPING[label_name + "_default"]
    _value = get_from_meta(meta, _key, _default)
    if _value:
        return Label(name=label_name, value=_value)
    return None


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
    return None


def get_node_status(test_result):
    status = test_result.data.run_result.status
    if status == "pass":
        return "passed"
    return "failed"


def get_title(node_info):
    meta = node_info.meta.fields
    return get_from_meta(meta, META_MAPPING["title_key"], node_info.node_name)


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


def get_labels(info):
    return [
        Label(name="framework", value="dbt"),
        Label(name="language", value="SQL"),
        Label(name="invocation_id", value=info.invocation_id),
        Label(name="pid", value=info.pid),
        Label(name="thread", value=info.thread),
    ]


def get_steps(test_result):
    status = get_node_status(test_result)
    timings = get_node_timings(test_result.data.node_info)
    steps = [
        TestStepResult(
            name=test_result.info.msg,
            status=status,
            **timings
        ),
    ]
    if test_result.data.run_result.message:
        steps.append(
            TestStepResult(
                name=test_result.data.run_result.message,
                status=status,
                **timings
            )
        )
    return steps


def get_node_timings(node_info):
    """"""
    start = datetime.fromisoformat(node_info.node_started_at).replace(
        tzinfo=timezone.utc).timestamp() * 1000
    stop = datetime.fromisoformat(node_info.node_finished_at).replace(
        tzinfo=timezone.utc).timestamp() * 1000
    return {"start": int(start), "stop": int(stop)}
