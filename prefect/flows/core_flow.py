from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
from prefect_dbt.cli.commands import trigger_dbt_cli_command
from prefect_great_expectations import run_checkpoint_validation


def log_start(logger):
    logger.info("Starting Staging ELT")
    debug_output = trigger_dbt_cli_command(
        command="dbt debug", 
        project_dir="../dbt/carpe_spike"
    )
    logger.info(debug_output)

def run_snapshots():
    """
    Runs dbt snapshot command
    """
    return trigger_dbt_cli_command(
        command="dbt snapshot --models core.*", 
        project_dir="../dbt/carpe_spike",
    )

def run_etl():
    return trigger_dbt_cli_command(
        command="dbt run --models core.*", 
        project_dir="../dbt/carpe_spike"
    )

def run_tests():
    """
    Runs dbt tests
    """
    return trigger_dbt_cli_command(
        command="dbt test --models core.*", 
        project_dir="../dbt/carpe_spike"
    )


def run_expectations():
    """
    Runs a Great Expectations checkpoint against core tables
    """
    return run_checkpoint_validation(
        checkpoint_name="core",
        data_context_root_dir="../great_expectations/"
    )


@flow(
    name="Core ELT",
    description="Runs flow for Core tables",
    task_runner=SequentialTaskRunner()
)
def core_etl_flow():
    logger = get_run_logger()
    log_start(logger)
    logger.info(run_snapshots())
    logger.info(run_etl())
    logger.info(run_tests())
    logger.info(run_expectations())


if __name__ == "__main__":
    core_etl_flow()