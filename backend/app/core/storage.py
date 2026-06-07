import boto3
from botocore.config import Config
from app.config import settings

_s3_client = None


def get_s3_client():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            endpoint_url=settings.storage_endpoint,
            aws_access_key_id=settings.storage_access_key,
            aws_secret_access_key=settings.storage_secret_key,
            region_name=settings.storage_region,
            config=Config(signature_version="s3v4"),
        )
    return _s3_client


async def upload_file(key: str, data: bytes, content_type: str = "image/png") -> str:
    client = get_s3_client()
    client.put_object(
        Bucket=settings.storage_bucket,
        Key=key,
        Body=data,
        ContentType=content_type,
    )
    return f"{settings.storage_endpoint}/{settings.storage_bucket}/{key}"


async def delete_file(key: str) -> None:
    client = get_s3_client()
    client.delete_object(Bucket=settings.storage_bucket, Key=key)
