from prefect import flow
from prefect.task_runners import SequentialTaskRunner

from staging_flow import staging_elt_flow
from core_flow import core_elt_flow


@flow(
    name="ELT",
    description="Runs flow for all tables",
    task_runner=SequentialTaskRunner(),
    version="1.0.0"
)
def elt_flow(dbt_dir: str="../dbt/etl_spike", ge_dir: str="../great_expectations/"):
    staging_elt_flow(dbt_dir, ge_dir)
    core_elt_flow(dbt_dir, ge_dir)
    

if __name__ == "__main__":
    elt_flow()