import logging
import os
import yaml
import jsonschema
from jsonschema import validate


json_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "results_dir": {
      "type": "string",
      "default": "target/allure-results"
    },
    "clean_results": {
      "type": "boolean",
      "default": True
    }
  },
  "required": ["clean_results", "results_dir"]
}


def apply_defaults(config, schema):
    if "properties" in schema:
        for property_name, sub_schema in schema["properties"].items():
            if "default" in sub_schema and property_name not in config:
                config[property_name] = sub_schema["default"]
            elif sub_schema.get("type") == "object":
                config[property_name] = config.get(property_name, {})
                apply_defaults(config[property_name], sub_schema)


def load_and_validate_config(yaml_file_path, schema):
    try:
        with open(yaml_file_path, 'r') as file:
            config = yaml.safe_load(file)
        validate(instance=config, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        logging.error("DBT allure configuration validation Error:", e.message)
        raise e
    except FileNotFoundError as e:
        config = dict()
    return config


def load_actions(allure_config):
    allure_result_dir = allure_config.get("results_dir")
    logging.info("Running dbt with dbt-allure results directory: %s".format(allure_result_dir))
    if allure_config.get("clean_results"):
        import shutil
        shutil.rmtree(allure_result_dir, ignore_errors=True)


def get_configurations():
    yaml_file_path = os.environ.get("DBT_ALLURE_CONFIG_PATH", ".dbt_allure.yml")
    allure_config = load_and_validate_config(yaml_file_path, json_schema)
    apply_defaults(allure_config, json_schema)
    load_actions(allure_config)
    return allure_config
