import sys

from dbt.cli.main import dbtRunner

from dbt_allure import allure_callback

if __name__ == "__main__":
    dbt = dbtRunner(
        callbacks=[
            allure_callback,
        ]
    )
    dbt.invoke(sys.argv[1:])
