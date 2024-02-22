import logging
import os
from pathlib import Path

import jsonschema
import yaml
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
        with Path(yaml_file_path).open("r") as file:
            config = yaml.safe_load(file)
        validate(instance=config, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        logging.error("DBT allure configuration validation Error:", e.message)
        raise e
    except FileNotFoundError:
        config = {}
    return config


yaml_file_path = os.environ.get("DBT_ALLURE_CONFIG_PATH", ".dbt_allure.yml")
ALLURE_CONFIGS = load_and_validate_config(yaml_file_path, json_schema)
apply_defaults(ALLURE_CONFIGS, json_schema)
