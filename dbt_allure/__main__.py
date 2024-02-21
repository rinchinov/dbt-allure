import sys
from dbt_allure import parse
from dbt.cli.main import dbtRunner


if __name__ == "__main__":
    configuration = configuration.get_configurations()
    dbt = dbtRunner(
        callbacks=[
            parse.allure_callback,
        ]
    )
    dbt.invoke(sys.argv[1:])
