from prefect import flow, get_run_logger

@flow
def test():
    logger = get_run_logger()
    logger.info('OK')


test()
