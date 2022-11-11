from prefect import flow, get_run_logger

VERSION = "1.0.0"

@flow(name="test", version=VERSION)
def test():
    logger = get_run_logger()
    logger.info(f"OK. VERSION: {VERSION}")
    return True
    

if __name__ == "__main__":
    test()