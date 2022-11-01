from prefect import flow
from prefect_great_expectations import run_checkpoint_validation

@flow
def api_flow():
    run_checkpoint_validation(
        checkpoint_name="staging",
        data_context_root_dir="../great_expectations/"
    )

api_flow()
