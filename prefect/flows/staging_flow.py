from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
from prefect_dbt.cli.commands import trigger_dbt_cli_command
from prefect_great_expectations import run_checkpoint_validation


def log_start(logger, dbt_dir):
    logger.info("Starting Staging ELT")
    debug_output = trigger_dbt_cli_command(
        command="dbt debug", 
        project_dir=dbt_dir,
    )
    logger.info(debug_output)

def run_snapshot(dbt_dir):
    """
    Runs dbt snapshot command
    """
    return trigger_dbt_cli_command(
        command="dbt snapshot", 
        project_dir=dbt_dir
    )

def run_etl(dbt_dir):
    return trigger_dbt_cli_command(
        command="dbt run --models staging.*", 
        project_dir=dbt_dir
    )

def run_tests(dbt_dir):
    """
    Runs dbt tests
    """
    return trigger_dbt_cli_command(
        command="dbt test --models staging.*", 
        project_dir=dbt_dir
    )


def run_expectations(ge_dir):
    """
    Runs a Great Expectations checkpoint against staging tables
    """
    return run_checkpoint_validation(
        checkpoint_name="staging",
        data_context_root_dir=ge_dir
    )


@flow(
    name="Staging ELT",
    description="Runs flow for Staging tables",
    task_runner=SequentialTaskRunner(),
    version="1.0.1"
)
def staging_elt_flow(dbt_dir: str="../dbt/etl_spike", ge_dir: str="../great_expectations/"):
    logger = get_run_logger()
    log_start(logger, dbt_dir)
    logger.info(run_snapshot(dbt_dir))
    logger.info(run_etl(dbt_dir))
    logger.info(run_tests(dbt_dir))
    logger.info(run_expectations(ge_dir))


if __name__ == "__main__":
    staging_elt_flow()