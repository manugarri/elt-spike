from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
from prefect_dbt.cli.commands import trigger_dbt_cli_command
from prefect_great_expectations import run_checkpoint_validation


def log_start(logger):
    logger.info("Starting Staging ELT")
    debug_output = trigger_dbt_cli_command(
        command="dbt debug", 
        project_dir="../dbt/etl_spike"
    )
    logger.info(debug_output)

def run_snapshot():
    """
    Runs dbt snapshot command
    """
    return trigger_dbt_cli_command(
        command="dbt snapshot", 
        project_dir="../dbt/etl_spike"
    )

def run_etl():
    return trigger_dbt_cli_command(
        command="dbt run --models staging.*", 
        project_dir="../dbt/etl_spike"
    )

def run_tests():
    """
    Runs dbt tests
    """
    return trigger_dbt_cli_command(
        command="dbt test --models staging.*", 
        project_dir="../dbt/etl_spike"
    )


def run_expectations():
    """
    Runs a Great Expectations checkpoint against staging tables
    """
    return run_checkpoint_validation(
        checkpoint_name="staging",
        data_context_root_dir="../great_expectations/"
    )


@flow(
    name="Staging ELT",
    description="Runs flow for Staging tables",
    task_runner=SequentialTaskRunner()
)
def staging_etl_flow() -> str:
    logger = get_run_logger()
    log_start(logger)
    logger.info(run_snapshot())
    logger.info(run_etl())
    logger.info(run_tests())
    logger.info(run_expectations())
    return "OK"


if __name__ == "__main__":
    staging_etl_flow()