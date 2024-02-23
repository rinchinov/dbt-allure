# dbt-allure

Enhance your dbt testing with the dbt-allure plugin. It transforms dbt test results into detailed Allure reports, giving clear insights into your data transformations. Perfect for ensuring data integrity, this plugin makes test outcomes easy to understand and act upon. Dive deeper into testing with dbt by checking the dbt testing documentation.

For more information on Allure, visit [Allure Framework](https://docs.qameta.io/allure/). To learn more about dbt and how it works, visit the [official dbt documentation](https://docs.getdbt.com/docs/introduction).

## Installation

Ensure you install the dbt-allure plugin with the same Python interpreter used by your dbt-core. The plugin can be installed via pip, poetry, or directly from a Git repository:

- **Using pip**
    ```bash
    pip install dbt-allure
    ```

- **Using Poetry**
    ```bash
    poetry add dbt-allure
    ```

## Usage

### Running dbt Commands to Generate Allure Test Results

The dbt-allure plugin can be utilized through programmatic invocations in Python or by using the provided dbt CLI wrapper.

**Programmatic Invocation:**

For more detailed information on programmatic invocation with dbt, refer to the [dbt documentation on running dbt programmatically](https://docs.getdbt.com/docs/running-a-dbt-project/running-dbt-in-python).

```python
from dbt_allure import DBTAllure
from dbt.cli.main import dbtRunner

dbt = dbtRunner(
    callbacks=[
        DBTAllure.callback,
    ]
)
dbt.invoke(["test"])
```

**CLI Wrapper (Bash):**


```bash
python -m dbt_allure test 
```
### Generating Allure Test Reports
To visualize your test results with Allure, generate and open the Allure report:

```bash
export TEST_RESULTS_DIR=target/allure-results
export TEST_REPORT_DIR=target/allure-report
allure generate $TEST_RESULTS_DIR -o $TEST_REPORT_DIR --clean
allure open $TEST_REPORT_DIR
```

### Plugin Configuration
The default configuration file for the plugin is .dbt_allure.yml, which can be overridden by the environment variable DBT_ALLURE_CONFIG_PATH.

**Configuration options**
* `results_dir_path`: The path where Allure results will be stored.
* `clean_results`: A boolean flag to clean results_dir_path before a run. Note: When using programmatic invocation, cleanup occurs only upon importing the callback. It's recommended to set this to False and manage cleanup manually for programmatic usage.