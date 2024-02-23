import sys

from dbt.cli.main import dbtRunner

from dbt_allure import DBTAllure

if __name__ == "__main__":
    dbt = dbtRunner(
        callbacks=[
            DBTAllure.callback,
        ]
    )
    dbt.invoke(sys.argv[1:])
