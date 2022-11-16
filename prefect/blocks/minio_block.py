"""
Creates minio storage bucket and prefect block

You can create buckets programatically in minio as well

from minio import Minio

client = Minio(
    "localhost:9000",
    access_key=MINIO_KEY,
    secret_key=MINIO_SECRET,
)

# Create bucket.
client.make_bucket(BUCKET_NAME)
"""
from minio import Minio
from prefect.filesystems import RemoteFileSystem

MINIO_ENDPOINT = "http://localhost:9000" 
MINIO_KEY = "minioadmin"
MINIO_SECRET = "minioadmin"
BUCKET_NAME = "prefect-flows"
BLOCK_NAME = "dev"

minio_block = RemoteFileSystem(basepath=f"s3://{BUCKET_NAME}/dev", 
                         settings={"key": MINIO_KEY, "secret": MINIO_SECRET,
                          "client_kwargs": {"endpoint_url": MINIO_ENDPOINT}
                          }
                          )
minio_block.save(BLOCK_NAME, overwrite=True) 
