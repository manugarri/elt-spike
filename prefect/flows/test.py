from prefect import task, flow, get_run_logger

VERSION = "1.0.0"

import os

@task
def list_files(logger, startpath="."):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        logger.info('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            logger.info('{}{}'.format(subindent, f))

@flow(name="test", version=VERSION)
def test():
    logger = get_run_logger()
    list_files(logger)
    logger.info(f"OK. VERSION: {VERSION}")
    return True
    

if __name__ == "__main__":
    test()