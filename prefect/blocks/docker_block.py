from prefect.infrastructure.docker import DockerContainer

snowflake_runtime = DockerContainer(
    type='docker-container', 
    env={'EXTRA_PIP_PACKAGES': 's3fs,snowflake-connector-python==2.8.1'},
    name='snowflake-container',
    command=None, 
    image='prefecthq/prefect:2.6.7-python3.10', stream_output=True)
    
snowflake_runtime.save("snowflake", overwrite=True)