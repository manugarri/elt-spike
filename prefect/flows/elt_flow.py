from prefect import flow
from prefect.task_runners import SequentialTaskRunner

from staging_flow import staging_elt_flow
from core_flow import core_elt_flow


@flow(
    name="ELT",
    description="Runs flow for all tables",
    task_runner=SequentialTaskRunner()
)
def elt_flow() -> str:
    staging_elt_flow()
    core_elt_flow()
    

if __name__ == "__main__":
    elt_flow()