from prefect import flow
from prefect.task_runners import SequentialTaskRunner

from staging_flow import staging_etl_flow
from core_flow import core_etl_flow


@flow(
    name="ELT",
    description="Runs flow for all tables",
    task_runner=SequentialTaskRunner()
)
def etl_flow() -> str:
    staging_etl_flow()
    core_etl_flow()
    

if __name__ == "__main__":
    etl_flow()