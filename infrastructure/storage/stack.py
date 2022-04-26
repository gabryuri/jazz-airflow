import os

from aws_cdk import core
from aws_cdk import (
    aws_s3 as s3,
)

from storage.base import S3StorageBaseBucket, StorageLayer


class S3StorageStack(core.Stack):
    def __init__(self, scope: core.Construct, **kwargs):
        #self.deploy_env = os.environ["ENVIRONMENT"]
        super().__init__(scope, id=f"jazz-s3-storage-stack", **kwargs)

        self.s3_storage_landing = S3StorageBaseBucket(self, layer=StorageLayer.LANDING)

        self.s3_storage_processed = S3StorageBaseBucket(self, layer=StorageLayer.PROCESSED)

        self.s3_storage_metadata = S3StorageBaseBucket(self, layer=StorageLayer.METADATA)
