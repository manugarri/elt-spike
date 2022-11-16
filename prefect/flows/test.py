"""
Sample flow.

"""
from prefect import task, flow, get_run_logger

FLOW_NAME = "test"
FLOW_VERSION = "1.0.0"

import os

@task
def list_files(logger, startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        logger.info('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            logger.info('{}{}'.format(subindent, f))

@flow(name=FLOW_NAME, version=FLOW_VERSION)
def test(startpath="."):
    logger = get_run_logger()
    logger.debug(f"STARTING FLOW {FLOW_NAME}.{FLOW_VERSION}")
    logger.info(f"LOGGING FILES IN PATH '{startpath}'")
    list_files(logger, startpath)
    return True
    

if __name__ == "__main__":
    test()